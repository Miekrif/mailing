from telethon import TelegramClient, sync
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact
from telethon.errors import PeerFloodError, FloodWaitError
import os
import logging
from dotenv import load_dotenv
import uuid
import json
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Информационное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка")
load_dotenv(dotenv_path='.env')

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
phone = '+79961272158'

# Словарь с номерами телефонов и именами
users_v2 = {
    '+79286253895': 'Алиночка зайка'
    # Добавьте больше пользователей по необходимости
}


message = '''
Чайной Истории уже скоро 10 ЛЕТ 🔥

Мы уже поделились на своем канале новостями об акциях и предстоящих мероприятиях.

Присоединяйся к чайному коммьюнити, чтобы не пропустить самых вкусных пиал! 🍵 

➡️ https://t.me/chaystory ⬅️
'''

# # Генерация уникального идентификатора для имени сессии
# session_name = f'anon_{uuid.uuid4()}'

# Создание экземпляра TelegramClient
client = TelegramClient("mailing", api_id, api_hash)

with open("new_file.json", "r") as read_file:
    users = json.load(read_file)
    users = users['users']


# Функция для отправки сообщения пользователю по номеру телефона

def send_message_to_user(phone_number, message):
    try:
        # Импорт контактов
        contacts = [InputPhoneContact(client_id=0, phone=phone_number, first_name=f"{phone_number}", last_name="")]
        result = client(ImportContactsRequest(contacts))

        # Проверка наличия пользователей в списке
        while PeerFloodError:
            if result.users:
                # Получение ID пользователя
                user_id = result.users[0].id

                # Отправка сообщения
                client.send_message(user_id, message)

                # Добавление задержки перед отправкой следующего сообщения
                time.sleep(10)  # Задержка в 30 секунд, можно изменить по необходимости
            else:
                logger.warning(f"No users found for phone number: {phone_number}")
    except PeerFloodError as e:
        logger.error(f"Encountered PeerFloodError: {e}. Pausing message sending for a while.")
        time.sleep(100)
    except FloodWaitError as e:
        logger.error(f"Возникла ошибка FloodWaitError: {e}. Пауза на {e.seconds} секунд перед повторной попыткой.")
        time.sleep(e.seconds + 1)  # Добавляем 1 секунду к времени ожидания перед следующей попыткой


# Пример использования
if __name__ == '__main__':
    print(users)
    print(users_v2)
    # Вход в Telegram
    client.start(phone=phone)

    # Отправка сообщения каждому пользователю в словаре
    for phone_number, individual_message in users.items():
        send_message_to_user(phone_number, message)