import os

from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    DEBUG = True if os.environ["MODE"] == "development" else False
    CORS_ORIGINS = os.environ["ALLOWED_ORIGINS"].split(",")
    CORS_SUPPORTS_CREDENTIALS = True
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_NAME = "flask"
    # expiry dates
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    EMAIL_VERIFICATION_TOKEN_EXPIRY = "30,day"
    PASSWORD_RESET_TOKEN_EXPIRY = "1,day"
    # email
    MAIL_SERVER = os.environ["MAIL_SERVER"]
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    MAIL_DEFAULT_SENDER = os.environ["MAIL_USERNAME"]

    RATELIMIT_STORAGE_URI = os.environ["RATE_LIMIT_STORAGE"]

    # rate limiting



class ProductionConfig(Config):
    """Uses production database server."""

    DB_SERVER = "192.168.19.32"


class DevelopmentConfig(Config):
    DB_SERVER = "localhost"
