from outline.api_client import send_request
import json
import logging

logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def delete_key(key_id):
    send_request(method='DELETE', path=f'access-keys/{key_id}/')


async def list_all_keys():
    return send_request(method='GET', path='access-keys/').json()


async def add_key_to_srv(name):
    log.info('add_key_to_srv')
    key_id = await create_new_key()
    log.info(f'success, key_id = {key_id}')
    await rename_key(name, key_id)
    return await get_key_by_id(key_id)


async def create_new_key():
    new_key = send_request(method='POST', path='access-keys/').json()
    return new_key.get("id")


async def rename_key(name, key_id):
    data = {"name": name}
    send_request(method='PUT', path=f'access-keys/{key_id}/name', data=json.dumps(data))


async def get_key_by_id(key_id):
    keys = await list_all_keys()
    for key in keys.get('accessKeys'):
        if key.get("id") == key_id:
            return key
    return None


async def extract_access_url_from_key(key):
    return key.get('accessUrl')
