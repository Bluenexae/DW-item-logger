import json
import os

LOG_FILE = "items_log.json"

class ItemLogger:
    def __init__(self):
        self.logged_items = self.load_logged_items()

    def load_logged_items(self):
        """Load logged items from the JSON file."""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as file:
                return json.load(file)
        return {
            "Weapons": {},
            "Ammo": {},
            "Heals": {},
            "Stims": {},
            "Traps/Nades": {}
        }

    def save_logged_items(self):
        """Save the logged items to the JSON file."""
        with open(LOG_FILE, "w") as file:
            json.dump(self.logged_items, file, indent=4)

    def log_item(self, item_name, category="Weapons"):
        """Log an item under a given category."""
        if item_name in self.logged_items[category]:
            self.logged_items[category][item_name] += 1
        else:
            self.logged_items[category][item_name] = 1

        self.save_logged_items()
        print(f"Logged: {item_name} ({self.logged_items[category][item_name]}x) in {category}")

    def remove_item(self, item_name, category="Weapons"):
        """Remove an item from the log (undo feature)."""
        if item_name in self.logged_items[category]:
            self.logged_items[category][item_name] -= 1
            if self.logged_items[category][item_name] <= 0:
                del self.logged_items[category][item_name]
            self.save_logged_items()
            print(f"Removed: {item_name} from {category}")
        else:
            print(f"Item {item_name} not found in {category}")

    def show_log(self):
        """Print the current item log."""
        print(json.dumps(self.logged_items, indent=4))

# Example Usage (for testing)
if __name__ == "__main__":
    logger = ItemLogger()
    logger.log_item("Revolver", "Weapons")
    logger.log_item("Medkit", "Heals")
    logger.show_log()
    logger.remove_item("Revolver", "Weapons")
    logger.show_log()
