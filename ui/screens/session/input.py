from _curses import window

class SessionInput:
    """Draws the input section for the typing session."""

    def __init__(self, typing_session, stdscr: window, width: int):
        self.stdscr = stdscr
        self.width = width

        self.input_display = f"> {typing_session.current_input}"

    def draw(self):
        self.stdscr.addstr(9, (self.width - len(self.input_display)) // 2, self.input_display)
