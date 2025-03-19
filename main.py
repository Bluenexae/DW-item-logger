import pyautogui
import pytesseract
import numpy as np
import cv2
import collections
import re
import time
import tkinter as tk
import threading
import keyboard  # For detecting keypress

# Set Tesseract path (make sure this points to your Tesseract installation)
pytesseract.pytesseract.tesseract_cmd = r"c:\Users\12kal\Downloads\Tesseract-OCR\tesseract.exe"

# Log to store recognized items
logged_items = {
    "Weapons": collections.Counter(),
    "Ammo": collections.Counter(),
    "Heals": collections.Counter(),
    "Stims": collections.Counter(),
    "Traps/Nades": collections.Counter()
}

# Undo and Redo stacks
undo_stack = []
redo_stack = []

# Enable/Disable toggle
logging_enabled = True

# Fix text function to clean up recognized text
def fix_text(text):
    cleaned_text = text.strip()  # Remove leading and trailing spaces
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', cleaned_text)  # Remove non-alphanumeric characters except spaces
    return cleaned_text

# Function to capture a screenshot and extract text
def extract_text_from_screenshot():
    screenshot = pyautogui.screenshot(region=(860, 561, 198, 18))  # top_left (860, 561), bottom_right (1058, 579)
    screenshot_np = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
    
    # Run OCR
    extracted_text = pytesseract.image_to_string(screenshot_gray)
    return extracted_text

# Function to log recognized text
def log_text():
    if not logging_enabled:
        return  # If logging is disabled, skip the logging process

    extracted_text = extract_text_from_screenshot()

    # Fix the text by cleaning up unwanted characters
    corrected_text = fix_text(extracted_text).strip()

    # Discard certain items (e.g., "Crate", "Locker", "Knife")
    if corrected_text not in ["Crate", "Locker", "Knife"]:
        print(f"Logged text: {corrected_text}")

        # Choose category based on text, add to counter
        category = "Weapons"  # This can be adjusted to match your item categories
        logged_items[category][corrected_text] += 1

        # Save to undo stack
        undo_stack.append(('add', category, corrected_text))

        # Clear redo stack after a new item is added
        redo_stack.clear()

    else:
        print(f"Discarded item: {corrected_text}")

# Undo function
def undo():
    if undo_stack:
        action, category, item = undo_stack.pop()
        if action == 'add':
            # Remove the last added item
            logged_items[category][item] -= 1
            if logged_items[category][item] == 0:
                del logged_items[category][item]
            # Save the undo action to the redo stack
            redo_stack.append(('remove', category, item))

# Redo function
def redo():
    if redo_stack:
        action, category, item = redo_stack.pop()
        if action == 'remove':
            # Re-add the item
            logged_items[category][item] += 1
            # Save the redo action to the undo stack
            undo_stack.append(('add', category, item))

# Function to listen for the "e" key press and trigger logging
def listen_for_key():
    while True:
        if keyboard.is_pressed("e"):  # When the 'e' key is pressed
            print("E key pressed! Taking screenshot and logging item...")
            log_text()
            time.sleep(1)  # Add a slight delay to prevent multiple rapid presses

# Transparent GUI for organizing logged items
def create_gui():
    root = tk.Tk()
    root.title("Item Logger")
    root.geometry("400x400")  # Size of the window
    root.configure(bg="black")
    root.attributes("-topmost", True)  # Keep it above other windows
    root.attributes("-transparentcolor", "black")  # Make the background transparent
    
    # Add sections for organizing logged items
    weapons_label = tk.Label(root, text="Weapons", bg="black", fg="white", font=("Arial", 14))
    weapons_label.pack()
    
    ammo_label = tk.Label(root, text="Ammo", bg="black", fg="white", font=("Arial", 14))
    ammo_label.pack()
    
    heals_label = tk.Label(root, text="Heals", bg="black", fg="white", font=("Arial", 14))
    heals_label.pack()

    stims_label = tk.Label(root, text="Stims", bg="black", fg="white", font=("Arial", 14))
    stims_label.pack()

    traps_label = tk.Label(root, text="Traps/Nades", bg="black", fg="white", font=("Arial", 14))
    traps_label.pack()

    # Update the GUI with logged items
    def update_gui():
        weapons_label.config(text="Weapons: " + ", ".join([f"{item} {count}x" for item, count in logged_items["Weapons"].items()]))
        ammo_label.config(text="Ammo: " + ", ".join([f"{item} {count}x" for item, count in logged_items["Ammo"].items()]))
        heals_label.config(text="Heals: " + ", ".join([f"{item} {count}x" for item, count in logged_items["Heals"].items()]))
        stims_label.config(text="Stims: " + ", ".join([f"{item} {count}x" for item, count in logged_items["Stims"].items()]))
        traps_label.config(text="Traps/Nades: " + ", ".join([f"{item} {count}x" for item, count in logged_items["Traps/Nades"].items()]))
        root.after(1000, update_gui)  # Update every second
    
    update_gui()

    # Run the GUI
    root.mainloop()

# Start everything
if __name__ == "__main__":
    print("Starting up...")

    # Start GUI
    gui_thread = threading.Thread(target=create_gui)
    gui_thread.daemon = True
    gui_thread.start()

    # Start listening for keypress
    listen_for_key()
