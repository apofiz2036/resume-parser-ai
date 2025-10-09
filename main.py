import gspread
from google.oauth2.service_account import Credentials

from pprint import pprint

print("Запуск скрипта")

#Область доступа
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

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
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1UB0XkHuLRVPU040D8ViGKQEANTiH_sQwKlilCWIdipc/edit?gid=0#") #TODO убрать отсюда
sheet = spreadsheet.sheet1

data_from_sheet = sheet.get_all_values()
headers = data_from_sheet[0]

resume = 15
test_task = 16
paei = 17
telegram_id = 0

candidates = []

for row in data_from_sheet[1:]:
    candidate = {
        "telegram_id": row[telegram_id] if row[telegram_id] not in ['', '#VALUE!'] else None,
        "resume": row[resume] if row[resume] not in ['', '#VALUE!'] else None,
        "test_task": row[test_task] if row[test_task] not in ['', '#VALUE!'] else None,
        "paei": row[paei] if row[paei] not in ['', '#VALUE!'] else None,
    }
    candidates.append(candidate)

pprint(candidates)
