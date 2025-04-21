from _curses import window

class SessionHeader:
    """Header component for the typing session interface."""

    def __init__(self, typing_session, stdscr: window):
        self.typing_session = typing_session
        self.stdscr = stdscr
        self.width = stdscr.getmaxyx()[1]

        self.header = [
                  f"Shelltyping Session ({typing_session.time_limit}s)",
                  f"Time: {int(self.typing_session.time_limit - self.typing_session.elapsed_time)}s | WPM: {int(self.typing_session.stats.wpm)} | Accuracy: {int(self.typing_session.stats.accuracy)}%"
                ]

    def draw(self):
        """Draws the header for the typing session."""

        for i, line in enumerate(self.header):
            y_pos = i + 1
            if y_pos < self.width - 1:
                self.stdscr.addstr(y_pos, (self.width - len(line)) // 2, line)
