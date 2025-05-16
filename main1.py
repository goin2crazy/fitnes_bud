import subprocess
import time
import schedule
import random
import logging
import traceback  # Import traceback for detailed error info

from utils import send_notification, load_config
from network_access import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()          # Log to the console
    ]
)

# 👉 Your cute little squat function
def do_squats():
    try:
        from exercises_calculations import SquatExsercise
        logging.info("Starting squats exercise.")
        send_notification(f"Time for squats, sweetheart! 🍑 Let's go!", "I will watch you anyway. Go on i am counting!", emotion="serious")
        SquatExsercise().run()
        logging.info("Squats exercise completed successfully.")
    except Exception as e:
        logging.error(f"Error during squats: {e}")
        logging.error(traceback.format_exc())  # Log the full traceback

# 🌸 Full rest routine
def break_routine():
    try:
        logging.info("Starting break routine.")
        send_notification("Break Time!", "Internet will be disabled for a bit. Get ready to exercise! 😉", emotion="determined")  # Added image path
        disable_internet()
        do_squats()
        send_notification("Break Over", "Welcome back! Internet is re-enabled.", emotion="thankfull")  # Added image path
        enable_internet()
        logging.info("Break routine completed successfully.")
    except Exception as e:
        logging.error(f"Error during break routine: {e}")
        logging.error(traceback.format_exc()) # Log the full traceback

def upcoming_break_warning():
    try:
        logging.info("Sending upcoming break warning.")
        send_notification("Upcoming Break", "Get ready for your break in 5 minutes! Stretch a little~",
                         emotion="warning")  # Added image path
        logging.info("Upcoming break warning sent.")
    except Exception as e:
        logging.error(f"Error sending upcoming break warning: {e}")
        logging.error(traceback.format_exc())

def passed_routine_warning():
    try:
        logging.info("Sending passed routine warning.")
        send_notification("How are you feeling?", "Stay concentrated~!",
                         emotion="proud")  # Added image path
        logging.info("Passed routine warning sent.")
    except Exception as e:
        logging.error(f"Error sending passed routine warning: {e}")
        logging.error(traceback.format_exc())



if __name__ == "__main__":
    try:
        # START CODE!!!
        config = load_config()
        logging.info("Configuration loaded.")

        # 🕒 Run every hour
        schedule.every().hour.at(f":{config['break_time']}").do(break_routine)
        logging.info(f"Break routine scheduled for every hour at :{config['break_time']}.")

        # ⏰ Schedule a warning 15 minutes before each hourly break
        schedule.every().hour.at(f":{config['reminder_time']}").do(passed_routine_warning)
        schedule.every().hour.at(f":{config['warning_time']}").do(upcoming_break_warning)
        logging.info(f"Passed routine warning scheduled for every hour at :{config['reminder_time']}.")
        logging.info(f"Upcoming break warning scheduled for every hour at :{config['warning_time']}.")


        # In case if pc left with internet access disabled
        enable_internet()
        send_notification("App started", "Assistant is watching the time 🥰 Will make sure you stay healthy & focused~",
                         emotion="happy")
        logging.info("Application started. Internet enabled, startup notification sent.")

        while True:
            schedule.run_pending()
            time.sleep(config['time_check_rate'])  # Reduced CPU usage from ~100% to near 0%
    except Exception as e:
        logging.critical(f"Unhandled error in main loop: {e}")
        logging.critical(traceback.format_exc()) # Log the full traceback
