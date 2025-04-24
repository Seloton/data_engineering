import mysql.connector
import time
from datetime import datetime

# Настройки подключения к базе данных
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'mydatabase',
}


def fetch_data():
    # Подключение к базе данных
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Выполнение запроса
    cursor.execute("SELECT * FROM messages")  # Замените на ваш запрос
    data = cursor.fetchall()

    # Закрытие соединения
    cursor.close()
    conn.close()

    return data

def save_to_file(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/data_slice_{timestamp}.txt"
    with open(filename, 'w') as f:
        for row in data:
            f.write(','.join(map(str, row)) + '\n')

if __name__ == "__main__":
    while True:
        data = fetch_data()
        save_to_file(data)
        time.sleep(120)  # 2 минут
