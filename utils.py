from datetime import datetime, time, timedelta
import logging
import schedule
import time as t

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("schedule_task.log"),
        logging.StreamHandler()
    ]
)

def get_kst_time():
    # UTC 시간을 기준으로 한국 시간(KST, UTC+9)을 계산
    utc_now = datetime.utcnow()
    kst_now = utc_now + timedelta(hours=9)
    return kst_now

def is_market_open():
    kst_now = get_kst_time()
    market_start = time(9, 0, 0)  # 오전 9시
    market_end = time(15, 30, 0)  # 오후 3시 30분
    market_status = market_start <= kst_now.time() <= market_end
    logging.info(f"Market open check at {kst_now}: {'Open' if market_status else 'Closed'}")
    return market_status

def schedule_task(func, interval=1):
    logging.info(f"Task scheduled to run every {interval} hour(s).")
    schedule.every(interval).hours.do(func)
    while True:
        kst_now = get_kst_time()
        logging.info(f"Checking schedule at {kst_now}.")
        schedule.run_pending()
        t.sleep(1)
