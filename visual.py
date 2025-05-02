import tkinter as tk
from PIL import Image, ImageTk
import os

def crop_and_resize_image(image_path, target_size=(200, 200)):
    """
    Crops and resizes the image to the specified target size.  Handles errors
    if the file doesn't exist or isn't a valid image.

    Args:
        image_path (str): Path to the image file.
        target_size (tuple, optional): The target size (width, height).
            Defaults to (200, 200).

    Returns:
        Image.Image: The cropped and resized image, or None on error.
    """
    try:
        image = Image.open(image_path)
        # Use a more robust method to find the center and crop
        width, height = image.size
        left = (width - target_size[0]) / 2
        top = (height - target_size[1]) / 2
        right = (width + target_size[0]) / 2
        bottom = (height + target_size[1]) / 2

        # Ensure the crop coordinates are valid
        left = max(0, left)
        top = max(0, top)
        right = min(width, right)
        bottom = min(height, bottom)
        cropped_image = image.crop((left, top, right, bottom))
        resized_image = cropped_image.resize(target_size, Image.LANCZOS)  # Use LANCZOS for high-quality resizing
        return resized_image
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def create_sliding_window(root, image_path):
    """
    Creates a toplevel window with the given image, which slides in from the
    bottom right corner of the screen.

    Args:
        root (tk.Tk): The main Tkinter root window.  This is needed to get
            the screen dimensions, but the toplevel window is created
            independently of it.
        image_path (str): Path to the image file.
    """

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Initial position of the window (off-screen, bottom right)
    x = screen_width
    y = screen_height

    # Create the toplevel window.  It is created as a child of the root,
    # but it is positioned and behaves independently.
    sliding_window = tk.Toplevel(root)
    sliding_window.overrideredirect(True)  # Remove window decorations (title bar, etc.)
    sliding_window.geometry(f"{200}x{200}+{x}+{y}")  # Set initial size and position

    # Load and process the image
    resized_image = crop_and_resize_image(image_path)
    if resized_image is None:
        # Handle the error case where the image couldn't be loaded.
        # We destroy the toplevel window to prevent a broken UI.
        sliding_window.destroy()
        return

    # Convert the PIL image to a Tkinter PhotoImage
    tk_image = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(sliding_window, image=tk_image)
    image_label.image = tk_image  # Keep a reference to prevent garbage collection
    image_label.pack()

    # Set the window to be always on top
    sliding_window.attributes('-topmost', True)

    def slide_in():
        """
        Slides the window into view from the bottom right corner.
        """
        nonlocal x, y
        x -= 5  # Adjust the speed of the slide-in by changing the decrement value
        y -= 5  # Adjust the speed of the slide-in by changing the decrement value
        if x > screen_width - 200 and y > screen_height - 200:
            sliding_window.geometry(f"{200}x{200}+{x}+{y}")
            sliding_window.after(10, slide_in)  # Continue sliding
        else:
            sliding_window.geometry(f"{200}x{200}+{screen_width - 200}+{screen_height - 200}") #set the final position

    # Start the slide-in animation after a delay
    sliding_window.after(500, slide_in)  # Start sliding after 0.5 seconds

def main():
    """
    Main function to create the Tkinter application and start the sliding window.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main root window
    # Provide a default image path.  The user should replace this with the
    # actual path to their "kim.png" image.
    image_path = "character.png"  # <--- Replace with the actual path to your image
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}.  Please make sure the file exists.")
        # Optionally, you could create a dummy image here, or display an error message
        # in a Tkinter window.  For simplicity, we just exit.
        return

    create_sliding_window(root, image_path)
    root.mainloop()  # Keep the Tkinter event loop running (though the main window is hidden)

if __name__ == "__main__":
    main()
