import gspread
from google.oauth2.service_account import Credentials

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
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1UB0XkHuLRVPU040D8ViGKQEANTiH_sQwKlilCWIdipc/edit?gid=0#")

sheet = spreadsheet.sheet1
data_from_sheet = sheet.get_all_values()

for row in data_from_sheet:
    print(row)

