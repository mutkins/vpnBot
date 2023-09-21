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
base_url = os.environ.get('OUTLINE_API_URL')


def send_request(method='get', params=None, path='access-keys/', data=None):
    url = base_url + path
    request = Request(method=method, url=url, headers=header, params=params, data=data)
    with Session() as session:
        prepared_request = session.prepare_request(request)
        try:
            r = session.send(request=prepared_request, verify=False)
            r.raise_for_status()
            return r
        except exceptions.RequestException as e:
            log.error(e)
            raise e
