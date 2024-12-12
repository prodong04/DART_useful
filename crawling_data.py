import requests
from datetime import datetime
from utils import is_market_open
from LLM import LLM
from config import DART_API_KEY, CRAWLING_INTERVAL_MINUTES, SLACK_WEBHOOK_URL
import schedule
import time as t
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("dart_crawler.log"),
        logging.StreamHandler()
    ]
)

class DartCrawler:
    def __init__(self):
        self.llm = LLM()
        self.que = {}
        logging.info("DartCrawler initialized.")

    def fetch_disclosures(self):
        url = "https://opendart.fss.or.kr/api/list.json"
        params = {
            "crtfc_key": DART_API_KEY,
            "bgn_de": datetime.now().strftime("%Y%m%d"),
            "end_de": datetime.now().strftime("%Y%m%d"),
            "page_no": 1,
            "page_count": 100,
        }
        logging.info("Fetching disclosures from DART API with parameters: %s", params)
        try:
            response = requests.get(url, params=params)

            response.raise_for_status()
            logging.info("Disclosures fetched successfully.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error("Error fetching disclosures: %s", e)
            return {"list": []}

    def analyze_and_notify(self):
        disclosures = self.fetch_disclosures()
        logging.info("Analyzing disclosures: %d items found.", len(disclosures.get("list", [])))
        for disclosure in disclosures.get("list", []):
            print(disclosure)
            logging.debug("Processing disclosure: %s", disclosure)
            if "투자판단관련주요경영사항" in disclosure.get("report_nm", ""):
                logging.info("Investment-related disclosure found: %s", disclosure["report_nm"])
                corp_name = disclosure['corp_name']
                ticker = disclosure['stock_code']
                content = disclosure['report_nm']
                msg = f'corp_name_{corp_name}, ticker_{ticker}, content_{content}'
                try:
                    self.send_slack_notification(msg)
                except Exception as e:
                    logging.error("Error during analysis: %s", e)
            elif "단일판매" or "공급계약체결" in disclosure.get("report_nm", ""):
                logging.info("Investment-related disclosure found: %s", disclosure["report_nm"])
                corp_name = disclosure['corp_name']
                ticker = disclosure['stock_code']
                content = disclosure['report_nm']
                msg = f'corp_name_{corp_name}, ticker_{ticker}, content_{content}'
                try:
                    self.send_slack_notification(msg)
                except Exception as e:
                    logging.error("Error during analysis: %s", e)


    def send_slack_notification(self, message):
        logging.info("Sending Slack notification with message: %s", message)
        payload = {
            "text": f"*DART 공시 분석 결과*\n\n{message}"
        }
        try:
            response = requests.post(SLACK_WEBHOOK_URL, json=payload)
            response.raise_for_status()
            logging.info("Slack notification sent successfully.")
        except requests.exceptions.RequestException as e:
            logging.error("Error sending Slack notification: %s", e)


def job():
    #if is_market_open():
    logging.info("Market is open. Starting job.")
    crawler = DartCrawler()
    crawler.analyze_and_notify()
    # else:
    #     logging.info("Market is closed. Skipping job.")



if __name__ == "__main__":
    logging.info("Starting DART Crawler...")

    logging.info("Market is open. Starting job.")
    crawler = DartCrawler()
    crawler.analyze_and_notify()
