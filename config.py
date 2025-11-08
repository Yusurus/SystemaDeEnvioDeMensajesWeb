# config.py
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# --- Base de Datos ---
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# --- Email (Gmail) ---
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
EMAIL_REMITENTE_REAL = os.getenv('EMAIL_REMITENTE_REAL')
DIRECCION_RECOJO = os.getenv('DIRECCION_RECOJO')

# Límite de correos a enviar por LOTE (cada vez que aprietas el botón)
EMAIL_BATCH_LIMIT = 50

# Límite MÁXIMO de correos a enviar por DÍA (para proteger la cuenta)
EMAIL_DAILY_LIMIT = 150