import os
from dotenv import load_dotenv
load_dotenv()
SUPPORT_BOT_USERNAME = '@duckySupport_bot'
SUPPORT_BOT_LINK = 'https://t.me/duckySupport_bot'
# PROXY = 'socks5://localhost:1080'
PROXY = None
HOSTS_TO_CHECK = ["https://ya.ru", "https://google.com", "https://www.youtube.com", "https://instagram.com", "https://facebook.com"]
TIME_TO_CHECK_EXPIRED_KEYS = '12:00'
TIME_TO_CHECK_INACTIVE_KEYS = '15:00'
TRIAL_KEY_LOCATION = "UAE"
TRIAL_SERVER_NAME = "UAE_1"
SERVERS = [
    {
        "country": "Finland",
        "flag": "🇫🇮",
        "name": "Finland_1",
        "api_url": os.environ.get('FINLAND_1_API_URL'),
        "price": [
            {
                "id": 1,
                "name_ru": "1 месяц",
                "desc_new_key": "подписка на 1 месяц",
                "desc_extend_key": "продление подписки на 1 месяц",
                "price": 200
            },
            {
                "id": 3,
                "name_ru": "3 месяца",
                "desc_new_key": "подписка на 3 месяца",
                "desc_extend_key": "продление подписки на 3 месяца",
                "price": 500
            },
        ]

    },
    {
        "country": "UAE",
        "flag": "🇦🇪",
        "name": "UAE_1",
        "api_url": os.environ.get('UAE_1_API_URL'),
        "price": [
            {
                "id": 1,
                "name_ru": "1 месяц",
                "desc_new_key": "подписка на 1 месяц",
                "desc_extend_key": "продление подписки на 1 месяц",
                "price": 200
            },
            {
                "id": 3,
                "name_ru": "3 месяца",
                "desc_new_key": "подписка на 3 месяца",
                "desc_extend_key": "продление подписки на 3 месяца",
                "price": 500
            },
        ]

    }
]
