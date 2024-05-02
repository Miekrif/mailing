import os
import logging
import time
import json
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact
from telethon.errors import PeerFloodError, FloodWaitError

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv(dotenv_path='.env')
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

# Загрузка пользователей из JSON-файла
with open("old.numbers.json", "r") as old_file:
    users_old = json.load(old_file)

with open("new_file.json", "r") as read_file:
    users = json.load(read_file)


# Инициализация клиента Telegram
client = TelegramClient("mailing", api_id, api_hash)

# Текст сообщения
message = ''' 
Чайной Истории уже скоро 10 ЛЕТ

Мы уже поделились на своем канале новостями об акциях и предстоящих мероприятиях.

Присоединяйся к чайному коммьюнити, чтобы не пропустить самых вкусных пиал!

➡️ https://t.me/chaystory ⬅️
'''

# Функция для отправки сообщения пользователю
async def send_message_to_user(phone_number, message):
    while True:
        try:
            # Импорт контактов
            contacts = [InputPhoneContact(client_id=0, phone=phone_number, first_name=f"{phone_number}", last_name="")]
            result = await client(ImportContactsRequest(contacts))

            if result.users:
                user_id = result.users[0].id
                await client.send_message(user_id, message)
                logger.info(f"Сообщение отправлено на {phone_number}")
                time.sleep(10)  # Пауза между сообщениями
                users_old['users_old'][phone_number] = ""
                write_new_old_numbers(users_old)
                break  # Выход из цикла при успешной отправке
            else:
                logger.warning(f"Не найдены пользователи по номеру телефона: {phone_number}")
                users_old['users_old'][phone_number] = ""
                write_new_old_numbers(users_old)
                break  # Выход из цикла, так как пользователь не найден
        except PeerFloodError as e:
            logger.error(f"Возникла ошибка PeerFloodError: {e}. Приостановка отправки сообщений на некоторое время.")
            logger.info(f"Повторная попытка отправки сообщения на {phone_number} через некоторое время.")
            time.sleep(1)  # Пауза перед следующей попыткой
        except FloodWaitError as e:
            logger.error(f"Возникла ошибка FloodWaitError: {e}. Пауза на {e.seconds} секунд перед повторной попыткой.")
            time.sleep(e.seconds + 1)  # Добавляем 1 секунду к времени ожидания перед следующей попыткой


def write_new_old_numbers(old_numbers):
    try:
        old_numbers_update = open("old.numbers.json", "w")
        if isinstance(dict, old_numbers):
            old_numbers_update.write(json.dumps(old_numbers))
        else: #list
            print('2')
            new_dict = {}
            new_dict["users"] = dict.fromkeys(old_numbers , '')
            old_numbers_update.write(json.dumps(new_dict))
        old_numbers_update.close()
    except Exception as e:
        logger.error(e)
    else:
        old_numbers_update.close()

# Основная функция
async def main():
    async with client:
        for phone_number, individual_message in users.items():
            if phone_number in users_old.keys():
                continue
            else:
                await send_message_to_user(phone_number, message)


if __name__ == '__main__':
    # Запуск клиента Telegram с указанным номером телефона
    client.start(phone=os.getenv('phone'))
    # Запуск основной функции
    client.loop.run_until_complete(main())
