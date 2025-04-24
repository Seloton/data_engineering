import os
import time

# Путь к директории с файлами
directory = '/Users/seloton/PycharmProjects/data_engineering/logs'  # Замените на ваш путь

def cleanup_old_files():
    current_time = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # Проверка, является ли файл старше 1 часа (3600 секунд)
        if os.path.isfile(file_path) and (current_time - os.path.getmtime(file_path)) > 300: # старше 5 мин
            os.remove(file_path)
            print(f"Удален файл: {file_path}")

if __name__ == "__main__":
    while True:
        cleanup_old_files()
        time.sleep(300)  # 5 мин
