from _curses import window

class SessionProgressBar:
    """Progress bar for the typing session."""
    def __init__(self, typing_session, stdscr: window):
        self.stdscr = stdscr

        width = stdscr.getmaxyx()[1]
        bar_width = width - 10

        progress = min(typing_session.elapsed_time / typing_session.time_limit, 1.0)
        filled_width = int(bar_width * progress)

        self.progress_bar = "█" * filled_width + "░" * (bar_width - filled_width)

    def draw(self):
        self.stdscr.addstr(3, 5, self.progress_bar)
