"""
TypingSession class - Core functionality for the typing session
"""

from datetime import datetime
import curses
import time

# Import custom modules
from utils.word_list import word_list

from .keystroke_recorder import KeystrokeRecorder
from .result_manager import ResultManager
from .statistics import TypingStats

class TypingSession:
    """Core functionality for the typing session."""

    def __init__(self, time_limit=60, word_source="common"):
        # Session metadata
        self.completed = False
        self.time_limit = time_limit
        self.word_source = word_source
        self.words = word_list(word_source)

        # Session state
        self.current_word_index = 0
        self.current_input = ""
        self.start_time = 0
        self.elapsed_time = 0

        # Advanced analytics
        self.stats = TypingStats()
        self.keystroke_recorder = KeystrokeRecorder()
        self.result_manager = ResultManager()
        self.word_start_time = 0  # Track when the current word started

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
        self.keystroke_recorder.record_keystroke(current_time, key)

        # Exit on ESC key
        if key == 27:
            self.completed = True
            return

        if key in (curses.KEY_BACKSPACE, 127, 8):  # Backspace keys
            if self.current_input:
                self.current_input = self.current_input[:-1]
                self.keystroke_recorder.record_backspace()
            return

        # Handle word when pressing Space key
        if key == ord(' '):
            self._process_word_completion(current_time)
            return

        # Regular character input
        if 32 <= key <= 126:  # Printable ASCII
            self.current_input += chr(key)

    def _process_word_completion(self, current_time):
        """Handle word completion when pressing Space key."""
        # Record time for the current word
        word_time = current_time - self.word_start_time
        self.keystroke_recorder.record_word_time(word_time)
        self.word_start_time = current_time

        # Check word accuracy
        current_word = self.words[self.current_word_index]
        self.stats.update_character_stats(self.current_input, current_word)

        # Move to next word
        self.current_word_index += 1
        if self.current_word_index >= len(self.words):
            self.completed = True

        self.current_input = ""

    def update_stats(self):
        """Update WPM and accuracy stats."""
        self.elapsed_time = time.time() - self.start_time

        if self.elapsed_time >= self.time_limit:
            self.completed = True

        if self.elapsed_time > 0:
            self.stats.calculate_wpm(self.elapsed_time)

    def save_result(self):
        """Save the test result to a JSON file."""

        result = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "wpm": round(self.stats.wpm, 2),
            "accuracy": round(self.stats.accuracy, 2),
            "time_limit": self.time_limit,
            "word_source": self.word_source,
            "elapsed_time": round(self.elapsed_time, 2),
            "consistency": round(self.stats.calculate_consistency(self.keystroke_recorder.word_times)),
        }

        self.result_manager.save_result(result)
