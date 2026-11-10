import os
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# Данные можно получить на https://my.telegram.org/
api_id = 1234567
api_hash = 'your_api_hash'

# ID пользователя, чат с которым вы хотите отслеживать
user_to_monitor = 123456789

# Папка, куда будут сохраняться все скачанные файлы
DOWNLOAD_PATH = 'download'


if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

client = TelegramClient('my_session', api_id, api_hash)


@client.on(events.NewMessage(chats=user_to_monitor))
async def auto_media_downloader(event):
    message = event.message
    
    if message.media and hasattr(message.media, 'ttl_seconds') and message.media.ttl_seconds is not None:
        
        sender_info = "мое" if message.out else "входящее"
        print("-" * 20)
        print(f"✅ ОБНАРУЖЕНО исчезающее медиа ({sender_info}). TTL: {message.media.ttl_seconds} сек.")
        print("Начинаю скачивание...")

        try:
            user_folder = os.path.join(DOWNLOAD_PATH, str(user_to_monitor))
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            file_path = await client.download_media(message, file=user_folder)
            print(f"✅ Файл успешно сохранен: {file_path}")

        except Exception as e:
            print(f"❌ ОШИБКА: Не удалось скачать файл: {e}")
    else:
        print(f". (Получено обычное сообщение ID: {message.id}, игнорирую)")


async def main():
    await client.start()
    print("\nКлиент успешно запущен.")
    print(f"Отслеживаю чат с пользователем ID: {user_to_monitor}")
    print(f"Исчезающие медиа будут сохраняться в папку '{DOWNLOAD_PATH}'")
    print("Для остановки работы нажмите Ctrl+C")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())