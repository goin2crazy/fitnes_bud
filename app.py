# app.py
import json

from flask import Flask, render_template, request
from flask import  jsonify

import os
import numpy as np 
import pandas as pd 

from visual_utils import * 
from utils import save_config 

app = Flask(__name__)

# Get the absolute path of the directory where this script is located
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
JSON_FILE_PATH = os.path.join(BASE_DIR, 'data.json')
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
    app_config_data = load_config() 

    # if request.method == 'POST':
    #     if 'settings.theme' in request.form:
    #         new_theme = request.form['settings.theme']
    #         if 'settings' not in app_config_data:
    #             app_config_data['settings'] = {}
    #         app_config_data['settings']['theme'] = new_theme

    #     notifications_enabled = 'settings.notifications' in request.form
    #     if 'settings' not in app_config_data:
    #         app_config_data['settings'] = {}
    #     app_config_data['settings']['notifications'] = notifications_enabled

    #     if save_data(app_config_data):
    #         app_config_data = load_data()
    #     else:
    #         if 'error' not in app_config_data:
    #              app_config_data['error_saving'] = "Could not save settings."

    activity_colors = load_activity_frequency()
    activity_categories = load_activities_types()

    return render_template(
        'main_page.html',
        app_data=app_config_data,
        activity_frequency_colors=activity_colors,
        activity_types_data=activity_categories
    )


# Assuming 'app' is your Flask application instance
# app = Flask(__name__) # Keep this line if 'app' is not defined elsewhere

@app.route('/changetiming/', methods=['POST'])
def change_timings():
    # Print the raw request body (as you had before)
    print("Raw Request Body:", request.data)

    # Parse the incoming JSON data from the request body
    request_data = request.get_json()

    # Check if JSON data was successfully parsed
    if request_data is None:
        return jsonify({
            'status': 'error',
            'message': 'Invalid JSON data received. Ensure Content-Type is application/json and body is valid JSON.'
        }), 400 # Bad Request status code

    print("Parsed Request Data:", request_data)

    try:
        # --- Configuration Loading and Updating ---

        # Load the current configuration settings using the defined function
        config = load_config()
        print("Current Config before update:", config)

        # Update config parameters with values from the request data
        # Ensure keys exist in both request_data and config before updating
        # Also, consider adding type checking/validation for request_data values
        if 'fitness-break' in request_data and 'break_time' in config:
            # You might want to add validation here to ensure the value is an integer or float
            config['break_time'] = request_data['fitness-break']
        if 'warning' in request_data and 'warning_time' in config:
             # You might want to add validation here
            config['warning_time'] = request_data['warning']
        if 'reminder' in request_data and 'reminder_time' in config:
             # You might want to add validation here
            config['reminder_time'] = request_data['reminder']

        print("Config after update:", config)

        # Save the updated configuration using the defined function
        save_success = save_config(config)

        # --- End Configuration Loading and Updating ---

        if save_success:
            # Return a success JSON response
            return jsonify({
                'status': 'success',
                'message': 'Operation done: Config updated and saved.',
                'updated_config': { # Return the updated values
                    'break_time': config.get('break_time'),
                    'warning_time': config.get('warning_time'),
                    'reminder_time': config.get('reminder_time')
                }
            }), 200 # OK status code
        else:
             # Return an error if saving failed
             return jsonify({
                'status': 'error',
                'message': 'Config updated but failed to save.',
                'updated_config': { # Optionally return the updated values even if save failed
                    'break_time': config.get('break_time'),
                    'warning_time': config.get('warning_time'),
                    'reminder_time': config.get('reminder_time')
                }
            }), 500 # Internal Server Error status code


    except Exception as e:
        # Catch any unexpected errors during the process
        print(f"An unexpected error occurred in change_timings: {e}")
        return jsonify({
            'status': 'error',
            'message': f'An unexpected error occurred: {e}'
        }), 500 # Internal Server Error status code

# /exercises_counts_settings
@app.route('/exercises_counts_settings/', methods=['POST'])
def change_exercises_counts_settings():
    # Print the raw request body (as you had before)
    print("Raw Request Body:", request.data)


if __name__ == '__main__':
    # Ensure you have a 'templates' directory with 'index.html' in it,
    # and a 'data.json' file in the same directory as app.py before running.
    app.run(debug=True)
