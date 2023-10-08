from db.access_keys import get_all_keys, mark_expired_key
from datetime import datetime
from outline.keys import delete_key
import logging
from dateutil.relativedelta import relativedelta
from tasks.exp_reminder import send_expired_msg


logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def check_inactive_keys():
    log.info('Time to check inactive keys')
    keys = get_all_keys(is_active=False)
    for key in keys:
        log.info(f'key {key.id} is inactive. Try to delete it in outline server')
        try:
            await delete_key(key_id=key.server_id)
            log.info(f'deleting successful')
        except Exception as e:
            if e.response.status_code == 404:
                log.info(f'Cant find the key {key.id} in outline server. Probably, it was already removed ')


async def check_expired_keys():
    log.info('Time to check expired keys')
    keys = get_all_keys(is_active=True)
    for key in keys:
        diff = (key.expired - datetime.today().date()).days
        if diff <= 3:
            log.info(f'key {key.id} expiring in diff days, send message')
            await send_expired_msg(chat_id=key.chat_id, key_id=key.id, days_to_expire=diff)
            if diff <= 0:
                await expire_key(key)


async def expire_key(key):
    log.info(f'key {key.id} is expied. Try to delete it from server and mark as expired in db')
    try:
        mark_expired_key(key_id=key.id)
        log.info(f'Mark it expired in db - SUCCESS')
        await delete_key(key_id=key.server_id)
        log.info(f'Delete it from server - SUCCESS')
    except Exception as e:
        log.error(f'ERROR WHEN TRY TO MARK EXPIRED KEY {e}')