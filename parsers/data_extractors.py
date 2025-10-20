from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

import logging
from logging_config import get_logger

from bs4 import BeautifulSoup

logger = get_logger(__name__)

def paei_scores(url, timeout=10):
    """
    Получает результаты PAEI теста по ссылке
    Возвращает словарь с баллами {P: 10, A: 20, E: 15, I: 5}
    """
    # Настройка браузера в фоновом режиме
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Запуск браузера
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        # Загрузка страницы
        driver.get(url)

        # Ждем пока загрузятся результаты теста
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".diagrams_item__head")))

        # Получаем HTML страницы
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Ищем все блоки с результатами
        result_blocks = soup.find_all("div", class_="diagrams_item__head")
        paei_scores = {}

        for block in result_blocks:
            text = block.get_text(strip=True)
            if "=" in text:
                letter, value = text.split("=")
                paei_scores[letter] = int(value)

        return paei_scores
             
    except Exception as e:
        error_message = f"Ошибка при парсинге PAEI: {e}"
        print(error_message)
        logger.warning(error_message)
        return None
    
    finally:
        driver.quit()

def extract_text_from_fdoc(url, creds_path="service_account.json"):
    """
    Извлекает текст из Google Docs документа по ссылке
    """
    try:
        # Извлекаем ID документа из ссылки
        doc_id = url.split("/d/")[1].split("/")[0]

        # Авторизация в Google Docs API
        creds = Credentials.from_service_account_file(creds_path)
        service = build("docs", "v1", credentials=creds)

        # Получаем документ
        document = service.documents().get(documentId=doc_id).execute()

        # Собираем текст из всех параграфов
        full_text = ""
        for content in document.get("body", {}).get("content", []):
            if "paragraph" in content:
                for element in content["paragraph"].get("elements", []):
                    full_text += element.get("textRun", {}).get("content", "")
        
        return full_text.strip()
    
    except Exception as e:
        error_message = f"Ошибка чтения текстового файла: {e}"
        print(error_message)
        logger.warning(error_message)
        return None