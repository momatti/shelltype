from _curses import window

class SessionInstructions:
    """Draws the instructions for the typing session."""

    def __init__(self, stdscr: window, width: int, height: int):
        self.stdscr = stdscr
        self.width = width
        self.height = height

    def draw(self):
        """Draws the instructions for the typing session."""

        instructions = "Press ESC to exit | BACKSPACE to delete | SPACE to submit word"
        self.stdscr.addstr(self.height - 2, (self.width - len(instructions)) // 2, instructions)
