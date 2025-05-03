import os
import subprocess
import signal
import sys
import asyncio
import traceback

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
        print("\nServer stopped on Ctrl+C.")
    finally:
        print("End of process...")
        os.kill(process_.pid, signal.SIGTERM)
        sys.exit(0)


if __name__ == "__main__":
    print("📦 Check MongoDB and creation of collections...")
    try:
        asyncio.run(upload_gyumri_data())
    except Exception as e:
        print("❌ Fail to load data from mongo:")
        traceback.print_exc()  # full stack
        print("Continue to run server...\n")
    process = start_server()
    handle_keyboard_interrupt(process)
