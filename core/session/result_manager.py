import os
import json

class ResultManager:
    """Manages saving and loading of typing test results."""

    def __init__(self):
        self.script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.history_dir = os.path.join(self.script_dir, "session", "history")
        os.makedirs(self.history_dir, exist_ok=True)
        self.history_file = os.path.join(self.history_dir, "typing_history.json")

    def save_result(self, result):
        """Save the test result to the history file."""
        try:
            # Read existing history
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []

            # Append new result and save
            history.append(result)
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)

        except Exception as e:
            print(f"Error saving results: {e}")

    def get_history(self):
        """Retrieve all historical results."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
        return []
