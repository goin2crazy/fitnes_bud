import time
import datetime
import schedule
import logging
import traceback

from utils import send_notification, load_config, load_exercise_logs
from network_access import enable_internet, disable_internet
from exercises_calculations import available_exercises

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# --- Helper Functions ---
def run_exercise(exercise_name, count, level, callbacks):
    if exercise_name not in available_exercises:
        logging.error(f"Error: '{exercise_name}' is not available.")
        return

    try:
        ExerciseClass = available_exercises[exercise_name]
        logging.info(f"Starting {exercise_name} exercise.")
        send_notification(
            f"Time for {exercise_name}, sweetheart! 🍑 Let's go!",
            "I will watch you anyway. Go on I am counting!",
            emotion="serious"
        )
        ExerciseClass(required_count=count, type=level, callbacks=callbacks).run()
        logging.info(f"{exercise_name} exercise completed successfully.")
    except Exception as e:
        logging.error(f"Error during {exercise_name}: {e}")
        logging.error(traceback.format_exc())


def do_level_exercises(level="base", callbacks=[]):
    config = load_config()
    exercises = config['normal_count'][level]
    for item in exercises:
        run_exercise(item['exercise'], item['count'], level, callbacks)


def do_base_level_exercises():
    do_level_exercises(level="base")


def do_mid_level_exercises():
    do_level_exercises(level="medium")


def was_mid_exercise_done_today():
    today = datetime.date.today()
    logs = load_exercise_logs()
    return any(
        log["type"] == "medium" and datetime.datetime.fromisoformat(log["timestamp"]).date() == today
        for log in logs
    )


def check_missed_mid_level_execution(scheduled_time):
    now = datetime.datetime.now()
    scheduled_dt = datetime.datetime.strptime(
        f"{now.strftime('%Y-%m-%d')} {scheduled_time}", "%Y-%m-%d %H:%M"
    )
    if now >= scheduled_dt and not was_mid_exercise_done_today():
        logging.warning("😿 Missed scheduled exercise… running it now anyway!")
        do_mid_level_exercises()


# --- Routine Functions ---
def break_routine():
    try:
        logging.info("Starting break routine.")
        send_notification("Break Time!", "Internet will be disabled for a bit. Get ready to exercise! 😉", emotion="determined")
        disable_internet()
        do_base_level_exercises()
        send_notification("Break Over", "Welcome back! Internet is re-enabled.", emotion="thankfull")
        enable_internet()
        logging.info("Break routine completed successfully.")
    except Exception as e:
        logging.error(f"Error during break routine: {e}")
        logging.error(traceback.format_exc())


def send_routine_warning(title, message, emotion):
    try:
        logging.info(f"Sending {title.lower()} warning.")
        send_notification(title, message, emotion=emotion)
    except Exception as e:
        logging.error(f"Error sending {title.lower()} warning: {e}")
        logging.error(traceback.format_exc())


def upcoming_break_warning():
    send_routine_warning("Upcoming Break", "Get ready for your break in 5 minutes! Stretch a little~", "warning")


def passed_routine_warning():
    send_routine_warning("How are you feeling?", "Stay concentrated~!", "proud")


# --- Main App Entry ---
if __name__ == "__main__":
    try:
        config = load_config()
        logging.info("Configuration loaded.")

        # Hourly routines
        schedule.every().hour.at(f":{config['break_time']}").do(break_routine)
        schedule.every().hour.at(f":{config['reminder_time']}").do(passed_routine_warning)
        schedule.every().hour.at(f":{config['warning_time']}").do(upcoming_break_warning)

        # Daily mid-level exercises
        schedule.every().day.at(config['medium_level_exercises_time']).do(do_mid_level_exercises)

        # Startup
        enable_internet()
        send_notification(
            "App started",
            "Assistant is watching the time 🥰 Will make sure you stay healthy & focused~",
            emotion="happy"
        )
        check_missed_mid_level_execution(config['medium_level_exercises_time'])
        logging.info("Application started. Internet enabled, startup notification sent.")

        while True:
            schedule.run_pending()
            time.sleep(config['time_check_rate'])

    except Exception as e:
        logging.critical(f"Unhandled error in main loop: {e}")
        logging.critical(traceback.format_exc())
