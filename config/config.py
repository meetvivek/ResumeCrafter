import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Security & Debug
SECRET_KEY = os.getenv("SECRET_KEY")

# Security & Debug
DEBUG = os.getenv("DEBUG", "").strip().lower() in ["true", "1", "yes"]

# Allowed Hosts (convert from comma-separated string to list)
ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host.strip()]

# Database Configuration
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")

# Time & Language
TIME_ZONE = os.getenv("TIME_ZONE")
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE")

BASE_BACK_URL= os.getenv("BASE_BACK_URL")

HOST = os.getenv("EMAIL_HOST")
PORT = os.getenv("EMAIL_PORT")
EMAIL_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
