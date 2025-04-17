class KeystrokeRecorder:
    """Records keystrokes and session actions (backspace, word completion, etc.)"""

    def __init__(self):
        self.backspaces = 0
        self.consistency = 0
        self.keystrokes = []
        self.word_times = []
        self.key_frequency = {}
        self.mistakes_by_char = {}

    def record_keystroke(self, timestamp, key):
        """Record a keystroke with its timestamp."""
        self.keystrokes.append((timestamp, key))

        # Update key frequency
        char_key = chr(key) if 32 <= key <= 126 else str(key)
        self.key_frequency[char_key] = self.key_frequency.get(char_key, 0) + 1

    def record_backspace(self):
        """Record use of backspace key."""
        self.backspaces += 1

    def record_word_time(self, time_taken):
        """Record time taken to type a word."""
        self.word_times.append(time_taken)


