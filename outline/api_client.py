import os
from requests import Request
from requests import Session
from requests import exceptions
import configparser
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")

load_dotenv()
header = {"Content-Type": "application/json"}


def send_request(server_name, method='get', params=None, path='access-keys/', data=None):

    match server_name:
        case 'Finland_1':
            base_url = os.environ.get('FINLAND_1_API_URL')
        case 'UAE_1':
            base_url = os.environ.get('UAE_1_API_URL')

    url = base_url + path
    request = Request(method=method, url=url, headers=header, params=params, data=data)
    with Session() as session:
        prepared_request = session.prepare_request(request)
        try:
            log.info(f'Send Request {prepared_request}')
            r = session.send(request=prepared_request, verify=False)
            r.raise_for_status()
            log.info(f'Response {r}')
            return r
        except exceptions.RequestException as e:
            log.error(e)
            raise e
