import json
import os
import pytesseract
from PIL import Image

# Define the path to Tesseract OCR (update this if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

LOG_FILE = "items_log.json"
CORRECTIONS_FILE = "corrections.json"

class ItemLogger:
    def __init__(self):
        self.logged_items = self.load_logged_items()
        self.correction_dict = self.load_corrections()

    def load_logged_items(self):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as file:
                return json.load(file)
        return {"Weapons": {}, "Ammo": {}, "Heals": {}, "Stims": {}, "Traps/Nades": {}, "Food": {}}  # Added "Food" category

    def save_logged_items(self):
        with open(LOG_FILE, "w") as file:
            json.dump(self.logged_items, file, indent=4)

    def load_corrections(self):
        if os.path.exists(CORRECTIONS_FILE):
            with open(CORRECTIONS_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_corrections(self):
        with open(CORRECTIONS_FILE, "w") as file:
            json.dump(self.correction_dict, file, indent=4)

    def add_correction(self, incorrect_name, correct_name):
        self.correction_dict[incorrect_name] = correct_name
        self.save_corrections()

    def fix_item_name(self, item_name):
        return self.correction_dict.get(item_name, item_name)

    def log_item(self, item_name, category="Weapons"):
        corrected_name = self.fix_item_name(item_name)
        if corrected_name in self.logged_items[category]:
            self.logged_items[category][corrected_name] += 1
        else:
            self.logged_items[category][corrected_name] = 1
        self.save_logged_items()

    def extract_items_from_image(self, image_path, category="Weapons"):
        try:
            image = Image.open(image_path)
            extracted_text = pytesseract.image_to_string(image)
            items = extracted_text.split("\n")
            
            for item in items:
                item = item.strip()
                if item:
                    self.log_item(item, category)
        except Exception as e:
            print(f"Error processing image: {e}")

    def get_logged_items(self):
        return self.logged_items

# Example of fixing and logging an item
if __name__ == "__main__":
    item_logger = ItemLogger()

    # Add correction for "SEONS" to "BEANS" under the "Food" category
    item_logger.add_correction("SEONS", "BEANS")

    # Log "SEONS" (which should be corrected to "BEANS") under the "Food" category
    item_logger.log_item("SEONS", category="Food")

    # Print the logged items to check the results
    logged_items = item_logger.get_logged_items()
    print(logged_items)  # Should show "Food": {"BEANS": 1}
