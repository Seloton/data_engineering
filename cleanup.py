import os
import time

# Путь к директории с файлами
directory = '/Users/seloton/PycharmProjects/data_engineering'  # Замените на ваш путь

def cleanup_old_files():
    current_time = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # Проверка, является ли файл старше 1 часа (3600 секунд)
        if os.path.isfile(file_path) and (current_time - os.path.getmtime(file_path)) > 3600:
            os.remove(file_path)
            print(f"Удален файл: {file_path}")

if __name__ == "__main__":
    while True:
        cleanup_old_files()
        time.sleep(3600)  # 1 час
