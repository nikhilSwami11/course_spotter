
import requests
import time
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = '8446431956'

COURSES_TO_MONITOR = ['572', '573', '578']
SUBJECT = 'CSE'
TERM = '2261'

# API Headers (mimicking a browser request to avoid 401)
HEADERS = {
    'authority': 'eadvs-cscc-catalog-api.apps.asu.edu',
    'accept': '*/*',
    'authorization': 'Bearer null',
    'origin': 'https://catalog.apps.asu.edu',
    'referer': 'https://catalog.apps.asu.edu/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def send_telegram_alert(message):
    """Sends a message to the specified Telegram user."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logger.info(f"Telegram notification sent: {message}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram message: {e}")

def check_seat_availability(catalog_nbr):
    """Checks seat availability for a specific course."""
    url = "https://eadvs-cscc-catalog-api.apps.asu.edu/catalog-microservices/api/v1/search/classes"
    params = {
        'refine': 'Y',
        'catalogNbr': catalog_nbr,
        'subject': SUBJECT,
        'term': TERM
    }

    try:
        logger.info(f"Checking {SUBJECT} {catalog_nbr}...")
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        classes = data.get('classes', [])
        if not classes:
            logger.warning(f"No classes found for {SUBJECT} {catalog_nbr}")
            return

        for cls in classes:
            # Check main seat info
            seat_info = cls.get('seatInfo', {})
            enrl_cap = seat_info.get('ENRL_CAP', 0)
            enrl_tot = seat_info.get('ENRL_TOT', 0)
            
            course_title = cls.get('CLAS', {}).get('COURSETITLELONG', 'Unknown Title')
            class_nbr = cls.get('CLAS', {}).get('CLASSNBR', 'Unknown')
            
            # Filter by specific Class Numbers (User provided list)
            # 22907: CSE 572
            # 37582: CSE 573
            # 27108: CSE 578
            TARGET_CLASS_NBRS = ['22907', '37582', '27108']
            
            if class_nbr not in TARGET_CLASS_NBRS:
                 logger.info(f" - Skipping {course_title} ({class_nbr}): Not in target list")
                 continue

            logger.info(f" - {course_title} ({class_nbr}): {enrl_tot}/{enrl_cap} enrolled")

            if enrl_tot < enrl_cap:
                msg = f"🚨 SEAT AVAILABLE! 🚨\n\nCourse: {SUBJECT} {catalog_nbr}\nTitle: {course_title}\nClass #: {class_nbr}\nSeats: {enrl_tot}/{enrl_cap}\n\nRegister now!"
                send_telegram_alert(msg)
                logger.info("Seat available! Notification sent.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data for {SUBJECT} {catalog_nbr}: {e}")

import argparse

CHECK_INTERVAL = 120 # Check every 2 minutes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--single-run', action='store_true', help='Run once and exit')
    parser.add_argument('--duration', type=int, default=0, help='Run for N seconds then exit')
    args = parser.parse_args()

    logger.info("Starting ASU Course Monitor...")
    
    # Only send startup message if running in continuous loop mode (no duration/single-run)
    if not args.single_run and args.duration == 0:
        send_telegram_alert("🚀 ASU Course Monitor Started! Checking CSE 572, 573, 578...")
    
    start_time = time.time()
    
    while True:
        for course in COURSES_TO_MONITOR:
            check_seat_availability(course)
            time.sleep(2) # Short pause between requests to be polite
        
        if args.single_run:
            logger.info("Single run completed. Exiting.")
            break
            
        elapsed = time.time() - start_time
        if args.duration > 0 and elapsed >= args.duration:
            logger.info(f"Duration {args.duration}s completed. Exiting.")
            break
        
        logger.info(f"Sleeping for {CHECK_INTERVAL} seconds...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
