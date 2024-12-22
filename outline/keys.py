from outline.api_client import send_request
import json
import logging

logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def delete_key(key_server_id, server_name):
    # Тут вроде исправил
    send_request(method='DELETE', path=f'access-keys/{key_server_id}/', server_name=server_name)


async def list_all_keys(server_name):
    # Тут вроде исправил
    return send_request(method='GET', path='access-keys/', server_name=server_name).json()


async def add_key_to_srv(name, server_name):
    log.info('add_key_to_srv')
    key_id = await create_new_key(server_name=server_name)
    log.info(f'success, key_id = {key_id}')
    await rename_key(name, key_id, server_name)
    return await get_key_by_id(key_id, server_name=server_name)


async def create_new_key(server_name):
    # Тут вроде исправил
    new_key = send_request(method='POST', path='access-keys/', server_name=server_name).json()
    return new_key.get("id")


async def rename_key(name, key_id, server_name):
    # Тут вроде исправил
    data = {"name": name}
    send_request(method='PUT', path=f'access-keys/{key_id}/name', data=json.dumps(data), server_name=server_name)


async def get_key_by_id(key_id, server_name):
    keys = await list_all_keys(server_name=server_name)
    for key in keys.get('accessKeys'):
        if key.get("id") == key_id:
            return key
    return None


async def extract_access_url_from_key(key):
    return key.get('accessUrl')
