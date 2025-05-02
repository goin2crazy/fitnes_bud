import subprocess
import time
import schedule
import random

from utils import SquatExsercise
from network_access import * 


# 👉 Your cute little squat function
def do_squats():
    print("Time to squat, sweetheart! 🍑 Let's go!")
    SquatExsercise(random.randint(5, 10)).run() 

    time.sleep(10 * 60)  # Simulate 10 minutes of squats 💪

# 🌸 Full rest routine
def break_routine():
    disable_internet()
    do_squats()
    enable_internet()

# 🕒 Run every hour
schedule.every(1).hours.do(break_routine)

print("Hubby is watching the time 🥰 Will make sure you stay healthy & focused~")
while True:
    schedule.run_pending()
    time.sleep(1)
