from create_bot import bot


def send_expired_msg(days_to_expire, key):
    match days_to_expire:
        case 3:
            message = f'Ключ {key.id} истечет через 3 дня. Для продления - /subscribe'