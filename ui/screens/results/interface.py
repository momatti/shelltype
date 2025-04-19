"""
Results module - handles display of basic typing test results
"""

from _curses import window

class ResultsInterface:
    """Shows the basic results screen."""

    def __init__(self, typing_session, window: window):
        window.clear()
        self.window = window
        height, width = self.window.getmaxyx()

        # Calculate results
        total_chars = typing_session.stats.correct_chars + typing_session.stats.incorrect_chars

        title = "TYPING SESSION RESULTS"
        self.window.addstr(5, (width - len(title)) // 2, title)

        result_lines = [
            f"Time: {round(typing_session.elapsed_time, 1)}s / {typing_session.time_limit}s",
            "",
            f"WPM: {int(typing_session.stats.wpm)}",
            f"Accuracy: {round(typing_session.stats.accuracy, 1)}%",
            f"Consistency: {round(typing_session.stats.consistency, 1)}%",
            "",
            f"Correct characters: {typing_session.stats.correct_chars}",
            f"Incorrect characters: {typing_session.stats.incorrect_chars}",
            "",
            f"Total characters: {total_chars}",
            f"Words completed: {typing_session.current_word_index}",
            "",
            "Press ESC to end session...",
        ]

        for i, line in enumerate(result_lines):
            y_pos = 7 + i
            if y_pos < height - 1:  # Make sure we don't print outside the screen
                self.window.addstr(y_pos, (width - len(line)) // 2, line)

        self.window.refresh()
        self.watch_user_input()

    def watch_user_input(self):
        """Wait for user input to exit or continue."""
        while True:
            key = self.window.getch()
            if key == 27:
                return key  # Exit on ESC (27)
            elif key == 10: # Enter key
                return key
