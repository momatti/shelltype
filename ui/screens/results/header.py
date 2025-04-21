from _curses import window

class ResultsHeader:
    """Header for the results interface."""
    def __init__(self, typing_session, stdscr: window):
        self.stdscr = stdscr
        self.typing_session = typing_session
        self.width = stdscr.getmaxyx()[1]

        self.title = "SHELLTYPING SESSION RESULTS"

    def draw(self):
        self.stdscr.addstr(5, (self.width - len(self.title)) // 2, self.title) # Title
