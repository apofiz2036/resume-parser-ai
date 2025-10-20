import gspread

import logging
from logging_config import get_logger

from data_extractors import paei_scores, extract_text_from_fdoc
from docx_writer import save_and_upload
from gpt import ask_gpt
from config import (
    CREDS,
    SPREADSHEET_URL,
    COLUMN_RESUME,
    COLUMN_TEST_TASK,
    COLUMN_PAEI,
    COLUMN_LINK_RESULT,
    COLUMN_GRADE,
)

logger = get_logger(__name__)
def main():
    print("Запуск скрипта")
    logger.info("Запуск скрипта")

    # --- Авторизация ---
    try:
        client = gspread.authorize(CREDS)
        print("Авторизация успешна")
    except Exception as e:
        error_message = f"Ошибка авторизации: {e}"
        print(error_message)
        logger.error(error_message)
        return

    # --- Работа с таблицей ---
    try:
        spreadsheet = client.open_by_url(SPREADSHEET_URL)
        sheet = spreadsheet.sheet1
        print("Таблица открыта")
    except Exception as e:
        error_message = f"Ошибка при открытии таблицы: {e}"
        print(error_message)
        logger.error(error_message)
        return
    
    data_from_sheet = sheet.get_all_values()
    headers = data_from_sheet[0]

    print("Начало обработки кандидатов")

    # --- Основной цикл ---
    for i, row in enumerate(data_from_sheet[1:], start=1):
        # Пропускаем уже обработанных кандидатов
        if row[COLUMN_LINK_RESULT] not in ['', None]:
            continue
        
        paei_url = row[COLUMN_PAEI] if row[COLUMN_PAEI] not in ['', '#VALUE!'] else None
        resume_url = row[COLUMN_RESUME] if row[COLUMN_RESUME] not in ['', '#VALUE!'] else None
        test_task_url = row[COLUMN_TEST_TASK] if row[COLUMN_TEST_TASK] not in ['', '#VALUE!'] else None

        resume_result = None
        test_task_result = None
        paei_result = None

        # --- PAEI ---
        if paei_url:
            try:
                paei_result = paei_scores(paei_url)
            except Exception as e:
                print(f"Ошибка при получении PAEI для {paei_url}: {e}")
                logger.warning(f"Ошибка при получении PAEI: {e}")

        # --- Резюме ---
        if resume_url:
            try:
                resume_result = extract_text_from_fdoc(resume_url)
            except Exception as e:
                print(f"Ошибка при загрузке резюме ({resume_url}): {type(e).__name__}")
                logger.warning(f"Ошибка при загрузке резюме: {e}")

        # --- Тестовое задание ---
        if test_task_url:
            try:
                test_task_result = extract_text_from_fdoc(test_task_url)
            except Exception as e:
                print(f"Ошибка при извлечении тестового задания({test_task_url}): {type(e).__name__}")
                logger.warning(f"Ошибка при извлечении тестового задания: {e}")


        # --- Формируем данные кандидата ---
        candidate = {
            "resume": resume_result,
            "test_task": test_task_result,
            "paei": paei_result,
        }

        # --- Отправляем в GPT, сохраняем и выгружаем ---
        try:
            gpt_response = ask_gpt(candidate)
            link_to_doc, grade_result = save_and_upload(gpt_response)
            sheet.update_cell(i + 1, COLUMN_LINK_RESULT, link_to_doc)
            sheet.update_cell(i + 1, COLUMN_GRADE, grade_result)
            print(f"Обработан кандидат {i}: {grade_result}")
        except Exception as e:
            error_message = f"Ошибка при обработке кандидата {i}: {e}"
            print(error_message)
            logger.warning(error_message)

    print("Скрипт завершён")
    logger.info("Скрипт завершён")


if __name__ == "__main__":
    main()
