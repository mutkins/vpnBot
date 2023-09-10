from outline.api_client import send_request


async def list_all_keys():
    return send_request(method='GET', path='access-keys/').json()