import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ENV = os.getenv("ENV", "dev")

# Database
class DBConfiguration:
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")
    NAME = os.getenv("DB_NAME")
    HOST = os.getenv("DB_HOST")
    PORT = os.getenv("DB_PORT")

# Email
class EmailEnv:
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_STARTTLS = False if ENV == "local" else True
    MAIL_SSL_TLS = False
    USE_CREDENTIAL = False if ENV == "local" else True

