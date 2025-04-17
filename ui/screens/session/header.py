from _curses import window

class SessionHeader:
    """Header component for the typing session interface."""

    def __init__(self, typing_session, stdscr: window, width: int):
        self.typing_session = typing_session
        self.stdscr = stdscr
        self.width = width

    def draw(self):
        """Draws the header for the typing session."""

        header = f"Terminal Typing Test | Time: {int(self.typing_session.time_limit - self.typing_session.elapsed_time)}s | WPM: {int(self.typing_session.stats.wpm)} | Accuracy: {int(self.typing_session.stats.accuracy)}%"
        self.stdscr.addstr(1, (self.width - len(header)) // 2, header)
