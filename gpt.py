from dotenv import load_dotenv
import requests
from docx import Document
import os

import logging
from logging_config import get_logger

load_dotenv()
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
logger = get_logger(__name__)

def load_prompt():
    try:
        file_name = 'prompt.txt'
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        error_message = f"Ошибка при загрузке промпта {e}"
        print(error_message)
        logger.error(error_message)


def load_profile():
    try:
        doc = Document('profile.docx')
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        return text
    except Exception as e:
        error_message = f"Ошибка при загрузке профиля вакансии {e}"
        print(error_message)
        logger.error(error_message)
    

def ask_gpt(candidate_data):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "x-folder-id": YANDEX_FOLDER_ID,
    }

    profile = load_profile()

    prompt_text = f"""
    ОПИСАНИЕ ВАКАНСИИ:
    {profile}

    ДАННЫЕ КАНДИДАТА:
    
    РЕЗЮМЕ:
    {candidate_data.get('resume', 'Нет данных')}
    
    ТЕСТОВОЕ ЗАДАНИЕ:
    {candidate_data.get('test_task', 'Нет данных')}
    
    PAEI ПРОФИЛЬ:
    {candidate_data.get('paei', 'Нет данных')}
    
    {load_prompt()}
    """ 

    data = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt-lite",
        "messages": [
            {
                "role": "system", 
                "text": "Ты опытный, и очень строгий HR-специалист. Анализируй кандидатов на основе данных и требований вакансии."
            },
            {"role": "user", "text": prompt_text},
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        json_data = response.json()

        result_text = json_data["result"]["alternatives"][0]["message"]["text"]
        return result_text
    except Exception as e:
        error_message = f"Ошибка при запросе к YandexGPT: {e}"
        print(error_message)
        logger.warning(error_message)
        return None
