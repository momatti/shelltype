class TypingStats:
    """Manages typing statistics and calculations."""

    def __init__(self):
        self.correct_chars = 0
        self.incorrect_chars = 0
        self.wpm = 0
        """Account only for correct characters"""
        self.wpm_raw = 0
        """Account for both correct and incorrect characters"""
        self.accuracy = 100.0

    def update_character_stats(self, input_text, target_text):
        """Update character statistics based on comparison between input and target."""
        # Count correct and incorrect characters
        for i, (c1, c2) in enumerate(zip(input_text, target_text)):
            if c1 == c2:
                self.correct_chars += 1
            else:
                self.incorrect_chars += 1

        # Account for length differences
        diff = abs(len(input_text) - len(target_text))
        if len(input_text) < len(target_text):
            self.incorrect_chars += diff

    def calculate_consistency(self, word_times):
        """Calculate typing consistency score based on word times."""
        if not word_times or len(word_times) < 2:
            return 0

        # Simple consistency calculation based on variation in word times
        avg_time = sum(word_times) / len(word_times)
        variance = sum((t - avg_time) ** 2 for t in word_times) / len(word_times)

        # Lower variance means higher consistency
        self.consistency = 100 / (1 + variance)
        return self.consistency

    def calculate_wpm(self, elapsed_time):
        """Calculate words per minute and accuracy."""
        if elapsed_time <= 0:
            return

        # Total characters (correct and incorrect)
        word_raw = (self.correct_chars + self.incorrect_chars) / 5

        # Total characters (correct only)
        word = self.correct_chars / 5

        # Time in minutes
        time_in_minutes = elapsed_time / 60

        # Raw WPM calculation
        self.wpm_raw = word_raw / time_in_minutes

        # WPM calculation
        self.wpm = word / time_in_minutes

        # Accuracy calculation
        if word > 0:
            self.accuracy = (self.correct_chars / word) * 100
        else:
            self.accuracy = 100.0
