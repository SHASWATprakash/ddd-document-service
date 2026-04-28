from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    "ddd-document-service.onrender.com"
]

DATABASE_URL = os.getenv("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=True
    )
}

DATABASES["default"]["OPTIONS"] = {
    "sslmode": "require",
}