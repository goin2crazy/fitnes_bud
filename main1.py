import subprocess
import time
import schedule
import random

from utils import send_notification, load_config
from network_access import * 


# 👉 Your cute little squat function
def do_squats():
    from exercises_calculations import SquatExsercise

    send_notification(f"Time for squats, sweetheart! 🍑 Let's go!", "I will watch you anyway. Go on i am counting!", emotion="serious")
    
    SquatExsercise().run() 


# 🌸 Full rest routine
def break_routine():
    send_notification("Break Time!", "Internet will be disabled for a bit. Get ready to exercise! 😉", emotion="determined") # Added image path
    disable_internet()

    do_squats()

    send_notification("Break Over", "Welcome back! Internet is re-enabled.", emotion="thankfull") # Added image path
    enable_internet()

def upcoming_break_warning():
    send_notification("Upcoming Break", "Get ready for your break in 5 minutes! Stretch a little~", 
                      emotion="warning") # Added image path


def passed_routine_warning():
    send_notification("How are you feeling?", "Stay concentrated~!", 
                      emotion="proud") # Added image path


if __name__ == "__main__": 
    # START CODE!!! 
    config = load_config() 
    # 🕒 Run every hour
    schedule.every().hour.at(f":{config['break_time']}").hours.do(break_routine)

    # ⏰ Schedule a warning 15 minutes before each hourly break
    schedule.every().hour.at(f":{config['reminder_time']}").do(passed_routine_warning)
    schedule.every().hour.at(f":{config['warning_time']}").do(upcoming_break_warning)


    # In case if pc left with internet access disabled
    enable_internet() 
    send_notification("App started", "Assistant is watching the time 🥰 Will make sure you stay healthy & focused~", 
                    emotion="happy")
    while True:
        schedule.run_pending()
        
        time.sleep(5)  # Reduced CPU usage from ~100% to near 0%