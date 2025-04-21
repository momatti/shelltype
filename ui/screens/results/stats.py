from _curses import window

class ResultStats:
    """Displays the statistics of the results."""
    def __init__(self, typing_session, stdscr: window):
        self.stdscr = stdscr
        self.typing_session = typing_session

        total_chars = typing_session.stats.correct_chars + typing_session.stats.incorrect_chars

        self.results = [
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
        ]

    def draw(self):
        height, width = self.stdscr.getmaxyx()

        Y_OFFSET = 4
        for i, result in enumerate(self.results):
            y_pos = (height // 2) - Y_OFFSET + i
            if y_pos < height - 1:  # Make sure we don't print outside the screen
                self.stdscr.addstr(y_pos, (width - len(result)) // 2, result)
