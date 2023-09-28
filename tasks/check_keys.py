from db.access_keys import get_all_active_keys, mark_expired_key
from datetime import datetime
from outline.keys import delete_key
import logging
from dateutil.relativedelta import relativedelta

logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def check_keys():
    log.info('Time to check expired keys')
    keys = get_all_active_keys()
    for key in keys:

        if key.expired == datetime.today().date() + relativedelta(days=3):
            print('Через 3 дня истечет')
        elif key.expired == datetime.today().date() + relativedelta(days=2):
            print('Послезавтра истечет')
        elif key.expired == datetime.today().date() + relativedelta(days=1):
            print('Завтра истечет')
        elif key.expired <= datetime.today().date() + relativedelta(days=0):
            print('Сегодня истечет')
            expire_key(key)


async def expire_key(key):
    log.info(f'key {key.id} is expied. Try to delete it from server and mark as expired in db')
    try:
        await delete_key(key_id=key.id)
        log.info(f'Delete it from server - SUCCESS')
        mark_expired_key(key_id=key.id)
        log.info(f'Mark it expired in db - SUCCESS')
    except Exception as e:
        log.error(f'ERROR WHEN TRY TO MARK EXPIRED KEY {e}')