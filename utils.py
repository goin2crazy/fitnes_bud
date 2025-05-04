import platform

# depends on windows version 
# there can be win11toast, win10toast, and others 
from win11toast import toast

image_emotions = {
    "happy": "images/happy.ico", 
    "thankfull": "images/happy.ico", 
    "proud": "images/happy.ico", 
    "determined": "images/pouty.ico", 
    "serious": "images/pouty.ico", 
    "pouty": "images/pouty.ico", 
    "warning": "images/warning.ico"
}


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

