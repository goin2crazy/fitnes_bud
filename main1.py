import subprocess
import time
import schedule
import random

from utils import send_notification
from exercises_calculations import SquatExsercise
from network_access import * 


# 👉 Your cute little squat function
def do_squats():
    send_notification("Time to squat, sweetheart! 🍑 Let's go!", "I will watch you anyway. Go on i am counting!", emotion="serious")
    SquatExsercise(random.randint(5, 10)).run() 


def rest_in_mind(): 
    time.sleep(5 * 60)  # Rest mind for 10 minutes  💪

# 🌸 Full rest routine
def break_routine():
    send_notification("Break Time!", "Internet will be disabled for a bit. Get ready to exercise! 😉", emotion="determined") # Added image path
    disable_internet()

    do_squats()

    send_notification("Rest in mind", "Your pc will be fine sweetheart, go drink water or touch some grass idk...", emotion="pouty")
    rest_in_mind() 

    send_notification("Break Over", "Welcome back! Internet is re-enabled.", emotion="thankfull") # Added image path
    enable_internet()

def upcoming_break_warning():
    send_notification("Upcoming Break", "Get ready for your break in 15 minutes! Stretch a little~", 
                      emotion="warning") # Added image path


def passed_routine_warning():
    send_notification("How are you feeling?", "Stay concentrated~!", 
                      emotion="proud") # Added image path

# 🕒 Run every hour
schedule.every().hour.at(":00").hours.do(break_routine)

# ⏰ Schedule a warning 15 minutes before each hourly break
schedule.every().hour.at(":25").do(passed_routine_warning)
schedule.every().hour.at(":45").do(upcoming_break_warning)


# In case if pc left with internet access disabled
enable_internet() 
send_notification("App started", "Assistant is watching the time 🥰 Will make sure you stay healthy & focused~", 
                  emotion="happy")
while True:
    schedule.run_pending()
    time.sleep(1)

