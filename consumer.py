import redis
import mysql.connector
import json

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Подключение к MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydatabase"
)
cursor = db.cursor()

while True:
    # Чтение сообщения из Redis
    message = r.brpop('messages', timeout=0)  # Блокирующее извлечение
    if message:
        message_data = json.loads(message[1])
        # Запись в MySQL
        cursor.execute("INSERT INTO messages (message) VALUES (%s)", (message_data['message'],))
        db.commit()
        print(f"Inserted: {message_data['message']}")
