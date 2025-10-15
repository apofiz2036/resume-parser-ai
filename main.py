import gspread
from google.oauth2.service_account import Credentials

from pprint import pprint

from data_extractors import paei_scores, extract_text_from_fdoc
from docx_writer import save_and_upload
from gpt import ask_gpt

print("Запуск скрипта")

#Область доступа
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

#TODO подключить .env
try:
    creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
    print("Кредиты загружены")
except:
    print("Кредиты не загружены")
    exit()

#Создание клиента
try:
    client = gspread.authorize(creds)
    print("Авторизация успешна")
except:
    print("Авторизация неуспешна")
    exit()

#Открыть таблицу TODO вынести ссылку из кода
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1UB0XkHuLRVPU040D8ViGKQEANTiH_sQwKlilCWIdipc/") #TODO убрать отсюда
sheet = spreadsheet.sheet1

data_from_sheet = sheet.get_all_values()
headers = data_from_sheet[0]

resume = 15
test_task = 16
paei = 17

for i, row in enumerate(data_from_sheet[1:], start=1):
    paei_url = row[paei] if row[paei] not in ['', '#VALUE!'] else None
    resume_url = row[resume] if row[resume] not in ['', '#VALUE!'] else None
    test_task_url = row[test_task] if row[test_task] not in ['', '#VALUE!'] else None

    resume_result = None
    test_task_result = None
    paei_result = None

    if paei_url:
        try:
            paei_result = paei_scores(paei_url)
        except Exception as e:
            print(f"Ошибка при получении PAEI для {paei_url}: {e}")
            paei_result = None

    if resume_url:
        try:
            resume_result = extract_text_from_fdoc(resume_url)
        except Exception as e:
            resume_result = None

    if test_task_url:
        try:
            test_task_result = extract_text_from_fdoc(test_task_url)
        except Exception as e:
            test_task_result = None

    candidate = {
        "resume": resume_result,
        "test_task": test_task_result,
        "paei": paei_result,
    }

    save_and_upload(ask_gpt(candidate))

