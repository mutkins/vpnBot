import os
from dotenv import load_dotenv
load_dotenv()



PROXY = None
HOSTS_TO_CHECK = ["https://ya.ru", "https://google.com", "https://www.youtube.com", "https://instagram.com", "https://facebook.com"]
TIME_TO_CHECK_KEYS = '12:00'
TRIAL_KEY_LOCATION = "Finland"
TRIAL_SERVER_NAME = "Finland_1"
SERVERS = [
    {
        "country": "Finland",
        "flag": "🇫🇮",
        "name": "Finland_1",
        "api_url": os.environ.get('Finland_1_API_URL'),
        "price": [
            {
                "id": 1,
                "name_ru": "1 месяц",
                "desc_new_key": "подписка на 1 месяц",
                "desc_extend_key": "продление подписки на 1 месяц",
                "price": 150
            },
            {
                "id": 3,
                "name_ru": "3 месяца",
                "desc_new_key": "подписка на 3 месяца",
                "desc_extend_key": "продление подписки на 3 месяца",
                "price": 300
            },
        ]

    },
    {
        "country": "Russia",
        "flag": "🇷🇺",
        "name": "Russia_1",
        "api_url": os.environ.get('Finland_1_API_URL'),
        "price": [
            {
                "id": 1,
                "name_ru": "1 месяц",
                "desc_new_key": "подписка на 1 месяц",
                "desc_extend_key": "продление подписки на 1 месяц",
                "price": 150
            },
            {
                "id": 3,
                "name_ru": "3 месяца",
                "desc_new_key": "подписка на 3 месяца",
                "desc_extend_key": "продление подписки на 3 месяца",
                "price": 300
            },
        ]

    }
]
