import mysql.connector
from mysql.connector import Error
import csv
from datetime import datetime, timedelta
import argparse

# Параметры подключения к базе данных
DB_CONFIG = {
    'host': 'localhost',
    'database': 'mydb',
    'user': 'root',
    'password': 'root'
}


def create_connection():
    """Создает соединение с базой данных"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Ошибка подключения к MySQL: {e}")
        return None


def parse_date(date_str):
    """Парсит дату из строки в формате YYYY-MM-DD"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Некорректный формат даты. Используйте YYYY-MM-DD")


def get_aggregated_data(connection, start_date, end_date):
    """Получает агрегированные данные за указанный период"""
    try:
        cursor = connection.cursor(dictionary=True)

        # Получаем список всех дней в периоде
        date_range = []
        current_date = start_date
        while current_date <= end_date:
            date_range.append(current_date)
            current_date += timedelta(days=1)

        results = []
        prev_day_topics = 0

        for i, day in enumerate(date_range):
            # Количество новых аккаунтов за день
            cursor.execute(
                "SELECT COUNT(*) as new_accounts FROM users WHERE DATE(created) = %s",
                (day,)
            )
            new_accounts = cursor.fetchone()['new_accounts']

            # Общее количество сообщений за день
            cursor.execute(
                """SELECT COUNT(*) as total_messages FROM logs 
                WHERE DATE(time) = %s AND action_type = 'Написание сообщения'""",
                (day,)
            )
            total_messages_result = cursor.fetchone()
            total_messages = total_messages_result['total_messages'] if total_messages_result['total_messages'] else 0

            # Количество анонимных сообщений за день
            cursor.execute(
                """SELECT COUNT(*) as anon_messages FROM logs 
                WHERE DATE(time) = %s AND action_type = 'Написание сообщения' AND users_user_id IS NULL""",
                (day,)
            )
            anon_messages_result = cursor.fetchone()
            anon_messages = anon_messages_result['anon_messages'] if anon_messages_result['anon_messages'] else 0

            # Процент анонимных сообщений
            anon_percent = (anon_messages / total_messages * 100) if total_messages > 0 else 0

            # Количество созданных тем за день
            cursor.execute(
                """SELECT COUNT(*) as topics_created FROM logs 
                WHERE DATE(time) = %s AND action_type = 'Создание темы' AND server_response = 'Успешно'""",
                (day,)
            )
            topics_created_result = cursor.fetchone()
            topics_created = topics_created_result['topics_created'] if topics_created_result['topics_created'] else 0

            # Процентное изменение количества тем относительно предыдущего дня
            if i == 0:
                topic_change_percent = 0.0
            else:
                if prev_day_topics == 0:
                    topic_change_percent = 100.0 if topics_created > 0 else 0.0
                else:
                    topic_change_percent = ((topics_created) / prev_day_topics * 100)

            prev_day_topics += topics_created

            results.append({
                'day': day.strftime("%Y-%m-%d"),
                'new_accounts': new_accounts,
                'anon_messages_percent': round(anon_percent, 2),
                'total_messages': total_messages,
                'topic_change_percent': round(topic_change_percent, 2)
            })

        cursor.close()
        return results
    except Error as e:
        print(f"Ошибка при получении данных: {e}")
        return None


def save_to_csv(data, filename):
    """Сохраняет данные в CSV файл"""
    if not data:
        print("Нет данных для сохранения")
        return

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['day', 'new_accounts', 'anon_messages_percent', 'total_messages', 'topic_change_percent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in data:
                writer.writerow(row)

        print(f"Данные успешно сохранены в {filename}")
    except IOError as e:
        print(f"Ошибка при сохранении в CSV: {e}")


def main():
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description='Агрегация данных форума')
    parser.add_argument('start_date', help='Начальная дата периода (YYYY-MM-DD)')
    parser.add_argument('end_date', help='Конечная дата периода (YYYY-MM-DD)')
    parser.add_argument('--output', default='forum_stats.csv', help='Имя выходного CSV файла')

    args = parser.parse_args()

    try:
        # Парсим даты
        start_date = parse_date(args.start_date)
        end_date = parse_date(args.end_date)

        if start_date > end_date:
            print("Ошибка: начальная дата должна быть раньше конечной")
            return

        # Устанавливаем соединение с базой данных
        connection = create_connection()
        if connection is None:
            return

        # Получаем агрегированные данные
        data = get_aggregated_data(connection, start_date, end_date)

        if data:
            # Сохраняем в CSV
            save_to_csv(data, args.output)

    except ValueError as e:
        print(f"Ошибка: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()