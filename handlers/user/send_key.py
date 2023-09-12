from aiogram import Bot, Dispatcher, types
from create_bot import bot
from aiogram.types import InputFile


async def send_key_to_user(chat_id, access_url):
    file = InputFile("content/manual.png")
    await bot.send_photo(photo=file, caption=f'<b>Шаг 1: Скачайте приложение</b>\n'
                                f'<a href="https://play.google.com/store/apps/details?id=org.outline.android.client">Android</a> | '
                                f'<a href="https://itunes.apple.com/app/outline-app/id1356177741">iPhone</a> | '
                                f'<a href="https://s3.amazonaws.com/outline-releases/client/windows/stable/Outline-Client.exe">Windows</a> | '
                                f'<a href="https://s3.amazonaws.com/outline-releases/client/linux/stable/Outline-Client.AppImage">Linux</a> | '
                                f'<a href="https://itunes.apple.com/app/outline-app/id1356178125">macOS</a>\n'
                                f'<b>Шаг 2: Скопируйте ключ и вставьте в приложение</b>\n'
                                f'🔑Ключ: (нажми для копирования)\n'
                                f'<code>{access_url}</code>\n'
                                f'<b>Шаг 3: Подключайтесь и пользуйтесь</b>', chat_id=chat_id, parse_mode='HTML')



