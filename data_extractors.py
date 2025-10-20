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
import time

logger = get_logger(__name__)

def paei_scores(url, timeout=10):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".diagrams_item__head")))

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        items = soup.find_all("div", class_="diagrams_item__head")
        paei_scores = {}

        for item in items:
            text = item.get_text(strip=True)
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
    try:
        doc_id = url.split("/d/")[1].split("/")[0]

        creds = Credentials.from_service_account_file(creds_path)
        service = build("docs", "v1", credentials=creds)

        document = service.documents().get(documentId=doc_id).execute()

        text = ""
        for content in document.get("body", {}).get("content", []):
            if "paragraph" in content:
                for elem in content["paragraph"].get("elements", []):
                    text += elem.get("textRun", {}).get("content", "")
        
        return text.strip()
    except Exception as e:
        error_message = f"Ошибка чтения текстового файла: {e}"
        print(error_message)
        logger.warning(error_message)
        return None