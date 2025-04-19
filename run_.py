import os
import subprocess
import signal
import sys
import asyncio

from src.helpers.databases.mongo_db.mongo_collections.places.schema_ import create_collection_if_not_exists


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
        asyncio.run(create_collection_if_not_exists())

        process = start_server()
        handle_keyboard_interrupt(process)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)
