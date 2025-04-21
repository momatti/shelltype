from _curses import window

class SessionInput:
    """Draws the input section for the typing session."""

    def __init__(self, typing_session, stdscr: window):
        self.stdscr = stdscr
        self.width = stdscr.getmaxyx()[1]

        self.input_display = f"> {typing_session.current_input}"

    def draw(self):
        self.stdscr.addstr(9, (self.width - len(self.input_display)) // 2, self.input_display)
