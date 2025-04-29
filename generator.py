import random
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error

# Параметры подключения к базе данных
db_config = {
    'host': 'localhost',
    'database': 'mydb',
    'user': 'root',
    'password': 'root'
}

# Типы действий
ACTION_TYPES = {
    'create_topic': 'Создание темы',
    'write_message': 'Написание сообщения',
    'view_page': 'Просмотр страницы',
    'like_post': 'Лайк поста',
    'user_login': 'Вход пользователя'
}

# Минимальное количество действий каждого типа в день
MIN_ACTIONS_PER_TYPE = 5


def create_connection():
    """Создает соединение с базой данных"""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Ошибка подключения к MySQL: {e}")
        return None


def generate_users(connection, num_users=20):
    """Генерирует тестовых пользователей"""
    try:
        cursor = connection.cursor()

        # Очищаем таблицы перед генерацией новых данных
        cursor.execute("DELETE FROM logs")
        cursor.execute("DELETE FROM users")
        connection.commit()

        # Генерируем пользователей
        for i in range(1, num_users + 1):
            name = f"user_{i}"
            created = datetime.now() - timedelta(days=random.randint(1, 365))
            cursor.execute("INSERT INTO users (name, created) VALUES (%s, %s)", (name, created))

        connection.commit()
        cursor.close()
        return num_users
    except Error as e:
        print(f"Ошибка при генерации пользователей: {e}")
        return 0


def generate_logs(connection, days=30):
    """Генерирует логи действий"""
    try:
        cursor = connection.cursor()

        # Получаем список всех пользователей
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        if not user_ids:
            print("Нет пользователей в базе данных")
            return

        start_date = datetime.now() - timedelta(days=days)

        for day in range(days):
            current_date = start_date + timedelta(days=day)

            # Для каждого типа действия генерируем как минимум MIN_ACTIONS_PER_TYPE записей
            for action_key, action_name in ACTION_TYPES.items():
                # Определяем количество действий (минимум MIN_ACTIONS_PER_TYPE плюс случайное число)
                num_actions = MIN_ACTIONS_PER_TYPE + random.randint(0, 10)

                for _ in range(num_actions):
                    # Для создания темы должно быть 2 случая ошибки из-за отсутствия логина
                    if action_key == 'create_topic' and _ < 2:
                        user_id = None
                        response = "Ошибка: отсутствует логин"
                    # Для написания сообщения примерно равное распределение залогиненных и незалогиненных
                    elif action_key == 'write_message':
                        if random.choice([True, False]):
                            user_id = random.choice(user_ids)
                            response = "Успешно"
                        else:
                            user_id = None
                            response = "Ошибка: пользователь не залогинен"
                    # Для остальных действий выбираем случайного пользователя
                    else:
                        user_id = random.choice(user_ids)
                        response = "Успешно"

                    # Генерируем случайное время в течение дня
                    time = current_date + timedelta(
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59),
                        seconds=random.randint(0, 59)
                    )

                    # Вставляем запись в лог
                    cursor.execute(
                        "INSERT INTO logs (users_user_id, server_response, action_type, time) VALUES (%s, %s, %s, %s)",
                        (user_id, response, action_name, time)
                    )

        connection.commit()
        cursor.close()
        print(f"Сгенерированы логи за {days} дней")
    except Error as e:
        print(f"Ошибка при генерации логов: {e}")


def main():
    # Устанавливаем соединение с базой данных
    connection = create_connection()
    if connection is None:
        return

    try:
        # Генерируем пользователей
        num_users = generate_users(connection)
        print(f"Сгенерировано {num_users} пользователей")

        # Генерируем логи за 30 дней
        generate_logs(connection, 30)
    finally:
        if connection.is_connected():
            connection.close()
            print("Соединение с MySQL закрыто")


if __name__ == "__main__":
    main()