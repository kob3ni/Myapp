import os
import json
import datetime
import shutil
import subprocess
import zipfile
import yadisk

# Определение пути к файлу конфигурации
current_directory = os.path.dirname(__file__)
config_path = os.path.join(current_directory, "config.json")

# Загрузка параметров из config.json
with open(config_path) as config_file:
    config = json.load(config_file)

# Настройки базы данных
DB_NAME = config["DB_SETTINGS"]["DB_NAME"]
DB_USER = config["DB_SETTINGS"]["DB_USER"]
DB_PASSWORD = config["DB_SETTINGS"]["DB_PASSWORD"]
DB_HOST = config["DB_SETTINGS"]["DB_HOST"]
DB_PORT = config["DB_SETTINGS"]["DB_PORT"]

# Настройки Яндекс.Диска
YANDEX_TOKEN = config["YANDEX_DISK"]["YANDEX_TOKEN"]
YANDEX_DIR = config["YANDEX_DISK"]["YANDEX_DIR"]

# Директория для хранения резервной копии
BACKUP_DIR = "backup"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Генерация имени файлов
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_FILE = os.path.join(BACKUP_DIR, f"db_backup_{TIMESTAMP}.sql")
ZIP_NAME = os.path.join(BACKUP_DIR, f"db_backup_{TIMESTAMP}.zip")

def check_token_access(yandex_token):
    try:
        y = yadisk.YaDisk(token=yandex_token)
        # Проверяем доступ к корневой папке
        y.get_disk_info()
        print("Токен имеет доступ к Яндекс.Диску.")
    except yadisk.exceptions.YaDiskError as e:
        print(f"Ошибка при проверке токена: {e}")
        
def clean_backup_directory(directory):
    """Очищает директорию перед созданием новой резервной копии."""
    print("Очистка папки резервных копий...")
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f"Удален файл: {file_path}")
        except Exception as e:
            print(f"Ошибка при удалении файла {file_path}: {e}")
            
            
def create_zip_with_zip64(source_dir, zip_name):
    """Создает ZIP-архив с поддержкой ZIP64."""
    print("Архивирование началось...")
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        zf.write(source_dir, os.path.basename(source_dir))
    print("Архивирование завершено.")
    
def create_backup():
    """Создает резервную копию базы данных и архивирует ее."""
    try:
        print("Создание резервной копии базы данных...")
        # Создаем резервную копию с помощью pg_dump
        command = [
            r"E:\Postgres\bin\pg_dump.exe",
            f"--dbname=postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
            "--file", BACKUP_FILE
        ]
        subprocess.run(command, check=True)
        print(f"Резервная копия базы данных создана: {BACKUP_FILE}")

        # Архивируем резервную копию
        create_zip_with_zip64(BACKUP_DIR, ZIP_NAME)
        print(f"Архив создан: {ZIP_NAME}")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании резервной копии: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def upload_to_yandex_disk():
    """Загружает архив с резервной копией на Яндекс.Диск."""
    try:
        print("Загрузка резервной копии на Яндекс.Диск...")
        y = yadisk.YaDisk(token=YANDEX_TOKEN)

        # Создаем директорию, если она не существует
        if not y.exists(YANDEX_DIR):
            y.mkdir(YANDEX_DIR)

        # Загружаем файл
        y.upload(ZIP_NAME, f"{YANDEX_DIR}/db_backup_{TIMESTAMP}.zip")
        print(f"Файл успешно загружен на Яндекс.Диск: {YANDEX_DIR}/db_backup_{TIMESTAMP}.zip")
    except Exception as e:
        print(f"Ошибка при загрузке на Яндекс.Диск: {e}")

if __name__ == "__main__":
    check_token_access(YANDEX_TOKEN)
    clean_backup_directory(BACKUP_DIR)
    create_backup()
    upload_to_yandex_disk()
