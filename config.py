import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# --- Загрузка переменных окружения ---
load_dotenv()

# --- Google API ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

CREDS = Credentials.from_service_account_file(
    "service_account.json", 
    scopes=SCOPES,
)

SPREADSHEET_URL= "https://docs.google.com/spreadsheets/d/1UB0XkHuLRVPU040D8ViGKQEANTiH_sQwKlilCWIdipc/"

# --- Номера столбцов в таблице ---
COLUMN_RESUME = 0
COLUMN_TEST_TASK = 1
COLUMN_PAEI = 2
COLUMN_LINK_RESULT = 4
COLUMN_GRADE = 5

# --- Яндекс ---
YANDEX_DISK_TOKEN = os.getenv("YANDEX_DISK_TOKEN")
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
