"""
TypingSession class - Core functionality for the typing session
"""

from datetime import datetime
import curses
import time
import os
import json

# Import custom modules
from utils.word_list import word_list

class TypingSession:
    """Core functionality for the typing session."""

    def __init__(self, time_limit=60, word_source="common"):
        self.time_limit = time_limit
        self.word_source = word_source
        self.words = []
        self.current_word_index = 0
        self.current_input = ""
        self.correct_chars = 0
        self.incorrect_chars = 0
        self.start_time = 0
        self.elapsed_time = 0
        self.wpm = 0
        self.accuracy = 100.0
        self.completed = False

        # Advanced analytics
        self.keystrokes = []  # List of (timestamp, key) tuples
        self.word_times = []  # Time taken for each word
        self.word_start_time = 0  # Track when the current word started
        self.mistakes_by_char = {}  # Character-specific mistake tracking
        self.backspaces = 0  # Number of backspaces used
        self.consistency = 0  # Typing consistency score
        self.key_frequency = {}  # Count of each key pressed

        self.words = word_list(word_source)

    def start(self):
        """Initialize the session and start the timer."""
        self.start_time = time.time()
        self.word_start_time = self.start_time
        self.completed = False

    def process_key(self, key):
        """Process a key press during the typing session."""
        if self.completed:
            return

        # Record the keystroke timing
        current_time = time.time()
        self.keystrokes.append((current_time, key))

        # Update key frequency
        char_key = chr(key) if 32 <= key <= 126 else str(key)
        self.key_frequency[char_key] = self.key_frequency.get(char_key, 0) + 1

        # Exit on ESC key
        if key == 27:
            self.completed = True
            return

        if key in (curses.KEY_BACKSPACE, 127, 8):  # Backspace keys
            if self.current_input:
                self.current_input = self.current_input[:-1]
                self.backspaces += 1
            return

        # Handle word when pressing Space key
        if key == ord(' '):
            # Record time for the current word
            word_time = current_time - self.word_start_time
            self.word_times.append(word_time)
            self.word_start_time = current_time

            # Check if the word is correct
            current_word = self.words[self.current_word_index]
            if self.current_input == current_word:
                self.correct_chars += len(current_word)
            else:
                # Count correct characters in the word
                for i, (c1, c2) in enumerate(zip(self.current_input, current_word)):
                    if c1 == c2:
                        self.correct_chars += 1
                    else:
                        self.incorrect_chars += 1

                # Account for length differences
                diff = abs(len(self.current_input) - len(current_word))
                self.incorrect_chars += diff

            self.current_word_index += 1
            if self.current_word_index >= len(self.words):
                self.completed = True

            self.current_input = ""
            return

        # Regular character input
        if 32 <= key <= 126:  # Printable ASCII
            self.current_input += chr(key)

    def update_stats(self):
        """Update WPM and accuracy stats."""
        self.elapsed_time = time.time() - self.start_time

        if self.elapsed_time >= self.time_limit:
            self.completed = True

        if self.elapsed_time > 0:
            # WPM calculation (standard 5 chars per word)
            total_chars = self.correct_chars + self.incorrect_chars
            self.wpm = (total_chars / 5) / (self.elapsed_time / 60)

            # Accuracy calculation
            if total_chars > 0:
                self.accuracy = (self.correct_chars / total_chars) * 100
            else:
                self.accuracy = 100.0

    def save_result(self):
        """Save the test result to a JSON file."""
        result = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "wpm": round(self.wpm, 2),
            "accuracy": round(self.accuracy, 2),
            "time_limit": self.time_limit,
            "word_source": self.word_source,
            "elapsed_time": round(self.elapsed_time, 2)
        }

        script_dir = os.path.dirname(os.path.abspath(__file__))
        history_dir = os.path.join(script_dir, "history")

        # Create history directory if it doesn't exist
        os.makedirs(history_dir, exist_ok=True)

        history_file = os.path.join(history_dir, "typing_history.json")

        try:
            # Read existing history
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []

            # Append new result and save
            history.append(result)
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)

        except Exception as e:
            print(f"Error saving results: {e}")
