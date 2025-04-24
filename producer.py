import random
import string
import time
import redis
import json  # Добавляем модуль json для сериализации

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0)

while True:
    # Генерация случайного сообщения
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    # Сериализуем словарь в JSON-строку
    message_data = json.dumps({'message': message})

    # Отправляем в Redis
    r.lpush('messages', message_data)
    print(f"Sent: {message}")

    time.sleep(60)  # Ждать 1 минуту