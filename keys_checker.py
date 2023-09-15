import aioschedule
import asyncio
from db.access_keys import get_all_active_keys, mark_expired_key
from datetime import datetime
from outline.keys import delete_key
from Exceptions.Exceptions import ConsistencyException
import logging

logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def on_startup(_):
    asyncio.create_task(scheduler())


async def scheduler():
    aioschedule.every().day.at('12:05').do(check_keys)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def check_keys():
    log.info('Time to check expired keys')
    keys = get_all_active_keys()
    for key in keys:
        if key.is_trial and key.expired <= datetime.today().date():
            log.info(f'key {key.id} is expied. Try to delete it from server and mark as expired in db')
            try:
                await delete_key(key_id=key.id)
                log.info(f'Delete it from server - SUCCESS')
                mark_expired_key(key_id=key.id)
                log.info(f'Mark it expired in db - SUCCESS')
            except Exception as e:
                log.error(f'ERROR WHEN TRY TO MARK EXPIRED KEY {e}')


