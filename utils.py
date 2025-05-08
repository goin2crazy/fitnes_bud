import yaml 
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

