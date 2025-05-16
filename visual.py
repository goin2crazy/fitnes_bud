# app.py
import json
from flask import Flask, render_template, request
import os
import pandas as pd 

from utils import load_config 


app = Flask(__name__)

# Get the absolute path of the directory where this script is located
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
JSON_FILE_PATH = os.path.join(BASE_DIR, 'data.json')

def sum_count_per_day_dict(df: pd.DataFrame) -> dict:
    """
    Calculates the sum of the 'count' column per day and returns it as a dictionary.

    Assumes the input DataFrame has columns named 'timestamp' and 'count'.

    Args:
        df: A pandas DataFrame with 'timestamp' (datetime or convertible)
            and 'count' (numeric) columns.

    Returns:
        A dictionary where keys are dates (as pandas Timestamps) and
        values are the sum of 'count' for that day.
    """
    # Ensure the 'timestamp' column is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Drop rows where timestamp conversion failed
    df.dropna(subset=['timestamp'], inplace=True)

    # Set the timestamp as the index
    df = df.set_index('timestamp')

    # Resample by day ('D') and calculate the sum of the 'count' column
    daily_sum_series = df['count'].resample('D').sum()

    # Convert the pandas Series to a dictionary
    daily_sum_dict = daily_sum_series.to_dict()

    return daily_sum_dict

# --- New function to load activity frequency ---
def load_activity_frequency():
    """
    Simulates loading activity frequency data.
    Returns a list of RGB color tuples.
    Example: [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    """
    try: 
        config = load_config()
        dataset_path = config['dataset_path']
        
        if dataset_path.endswith("json"): 
            dataset = pd.read_json(dataset_path)
        elif dataset_path.endswith("csv"): 
            dataset = pd.read_csv(dataset_path)
        else: 
            assert ("Dataset is incorrect format")

        last_month_counts = sum_count_per_day_dict(dataset)
        print(last_month_counts)

        last_month_counts = list(last_month_counts.values())[-30:]
        
        max_count = max(last_month_counts)
        last_month_counts_normalized = [i/max_count for i in last_month_counts]

        last_month_counts_to_color = [(int(50+100* i), int(255*i), int(255*i)) for i in last_month_counts_normalized]

        return last_month_counts_to_color
        
    except Exception as e: 
        print(e)
        return [
            (15, 15, 15),
        ]

# --- New function to load activity types ---
def load_activities_types():
    """
    Simulates loading activity types.
    Returns a dictionary categorizing activities.
    """
    return {
        "Warm-up": ["Jumping Jacks", "Arm Circles", "Leg Swings"],
        "Strength - Lower Body": ["Squats", "Lunges", "Deadlifts (Bodyweight)"],
        "Strength - Upper Body": ["Push-ups", "Pull-up Assists", "Dips (Chair)"],
        "Core": ["Plank", "Crunches", "Russian Twists"],
        "Cool-down": ["Static Stretching", "Foam Rolling"]
    }

def load_data():
    """Loads general app data (like settings) from the JSON file."""
    try:
        with open(JSON_FILE_PATH, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        # If the file doesn't exist, create it with default settings
        print(f"{JSON_FILE_PATH} not found. Creating with default settings.")
        default_data = {
            "title": "My App Data",
            "settings": {
                "theme": "light",
                "notifications": False
            }
        }
        save_data(default_data) # Save it so it exists for next time
        return default_data
    except json.JSONDecodeError:
        return {"error": "Error decoding data.json. Please check its format."}

def save_data(data):
    """Saves general app data to the JSON file."""
    try:
        with open(JSON_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    app_config_data = load_data()

    if request.method == 'POST':
        if 'settings.theme' in request.form:
            new_theme = request.form['settings.theme']
            if 'settings' not in app_config_data:
                app_config_data['settings'] = {}
            app_config_data['settings']['theme'] = new_theme

        notifications_enabled = 'settings.notifications' in request.form
        if 'settings' not in app_config_data:
            app_config_data['settings'] = {}
        app_config_data['settings']['notifications'] = notifications_enabled

        if save_data(app_config_data):
            app_config_data = load_data()
        else:
            if 'error' not in app_config_data:
                 app_config_data['error_saving'] = "Could not save settings."

    activity_colors = load_activity_frequency()
    activity_categories = load_activities_types()

    return render_template(
        'main_page.html',
        app_data=app_config_data,
        activity_frequency_colors=activity_colors,
        activity_types_data=activity_categories
    )

if __name__ == '__main__':
    # Ensure you have a 'templates' directory with 'index.html' in it,
    # and a 'data.json' file in the same directory as app.py before running.
    app.run(debug=True)
