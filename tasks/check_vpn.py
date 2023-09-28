import logging
from cf_speedtest.cf_speedtest.speedtest import main as speedtest_start
import requests
from config import HOSTS_TO_CHECK, PROXY, TIME_TO_CHECK_KEYS
from handlers.admin.utils import send_error_report

logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def check_vpn():
    log.info('Check_vpn() started')
    if PROXY:
        PROXY_DICT = {'http': f'{PROXY}', 'https': f'{PROXY}'}

    else:
        PROXY_DICT = None
    log.info(f'Checking hosts {HOSTS_TO_CHECK}')
    report = "<b>VPN ERROR REPORT</b>\n"
    is_error = False
    for host in HOSTS_TO_CHECK:
        try:
            r = requests.get(host, proxies=PROXY_DICT)
            log.info(f'Ping to {host}...{r.status_code}')
            report += f'Ping to {host}...{r.status_code}\n'
        except Exception as e:
            log.error(f'Ping to {host}...ERROR {e}')
            report += f'Ping to {host}...<b>ERROR</b>\n'
            is_error = True
    if is_error:
        await send_error_report(report)
    log.info(f'speedtest_start() started')
    speeds = speedtest_start(proxy=PROXY)
    log.info(f'Download speed: {int(speeds["download_speed"]/1000000)}Mb/s')
    log.info(f'Upload speed: {int(speeds["upload_speed"]/1000000)}Mb/s')
    if speeds['download_speed'] < 10*1000000 or speeds['upload_speed'] < 10*1000000:
        log.warning(f'<b>VPN WARN REPORT</b>\n'
                    f'average speed {int(speeds["download_speed"]/1000000)}Mb/s / {int(speeds["upload_speed"]/1000000)}Mb/s')
        await send_error_report(f'<b>VPN WARN REPORT</b>\n'
                                f'average speed {int(speeds["download_speed"]/1000000)}Mb/s / {int(speeds["upload_speed"]/1000000)}Mb/s')