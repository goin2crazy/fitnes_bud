import os 
import yaml 
import json
import platform

# depends on windows version 
# there can be win11toast, win10toast, and others 
image_emotions = {
    "happy": "images/happy.ico", 
    "thankfull": "images/happy.ico", 
    "proud": "images/happy.ico", 
    "determined": "images/pouty.ico", 
    "serious": "images/pouty.ico", 
    "pouty": "images/pouty.ico", 
    "warning": "images/warning.ico"
}

def load_config(config_path="config.yaml"):
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing configuration file '{config_path}': {e}")
        return {}



# Define the save_config function
def save_config(config_data, filepath="config.yaml"):
    """Saves configuration data to a YAML file."""
    try:
        with open(filepath, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False)
        print(f"Config saved successfully to {filepath}")
    except yaml.YAMLError as e:
        print(f"Error saving config file {filepath}: {e}")
        # Handle save error (e.g., log it, return False)
        return False
    except Exception as e:
        print(f"An unexpected error occurred saving config file {filepath}: {e}")
        return False
    return True # Indicate success


def send_notification(title, message, emotion=False):
    """Sends a desktop notification on Windows."""
    if platform.system() == "Windows":
        try:
            from plyer import notification


            if emotion:
                image_path = image_emotions[emotion]
                notification.notify(
                    title=title,
                    message=message,
                    app_icon=image_path,  # Corrected parameter name
                    app_name="Fitness budy", 
                    toast=False, 
                    timeout=5,  # seconds
                )
            else:
                notification.notify(
                    title=title,
                    message=message,
                    timeout=5,  # seconds
                )
        except ImportError:
            print("Warning: 'plyer' library not found. Notifications will not be sent.  Please install it: pip install plyer")
    else:
        print("Info: Notifications are only supported on Windows for now.")


def load_exercise_logs():
    LOG_FILE = load_config()['dataset_path']
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)