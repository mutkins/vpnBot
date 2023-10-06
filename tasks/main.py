import aioschedule
import asyncio
from config import TIME_TO_CHECK_KEYS
from tasks.check_vpn import check_vpn
from tasks.check_keys import check_keys


async def scheduler():
    aioschedule.every(4).hours.do(check_vpn)
    aioschedule.every().minute.do(check_keys)
    # aioschedule.every().day.at(TIME_TO_CHECK_KEYS).do(check_keys)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
