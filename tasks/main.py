import aioschedule
import asyncio
from config import TIME_TO_CHECK_EXPIRED_KEYS, TIME_TO_CHECK_INACTIVE_KEYS
from tasks.check_vpn import check_vpn
from tasks.check_keys import check_expired_keys, check_inactive_keys


async def scheduler():
    # aioschedule.every(2).minutes.do(check_vpn)
    aioschedule.every(4).hours.do(check_vpn)
    # aioschedule.every().minute.do(check_expired_keys)
    # aioschedule.every().minute.do(check_inactive_keys)
    aioschedule.every().day.at(TIME_TO_CHECK_EXPIRED_KEYS).do(check_expired_keys)

    aioschedule.every().day.at(TIME_TO_CHECK_INACTIVE_KEYS).do(check_inactive_keys)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
