import os
import subprocess
import signal
import sys
import asyncio

from src.helpers.databases.mongo_db.mongo_image_files.gyumri_data import upload_gyumri_data


def start_server():
    command = [
        "uvicorn",
        "src.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload",
    ]
    return subprocess.Popen(command)


def handle_keyboard_interrupt(process_):
    try:
        process_.wait()
    except KeyboardInterrupt:
        print("\nСервер был остановлен с помощью Ctrl+C.")
    finally:
        print("Завершаем процесс...")
        os.kill(process_.pid, signal.SIGTERM)
        sys.exit(0)


if __name__ == "__main__":
    try:
        print("📦 Проверка MongoDB и создание коллекции...")
        asyncio.run(upload_gyumri_data())

        process = start_server()
        handle_keyboard_interrupt(process)
    except Exception as e:
        raise

