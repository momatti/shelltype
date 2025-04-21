from _curses import window


class ResultInstructions():
    """Instruction for the results screen."""
    def __init__(self, stdscr: window):
        self.stdscr = stdscr
        self.instructions = "Press enter to continue | Press ESC to exit..."

    def draw(self):
        height, width = self.stdscr.getmaxyx()
        self.stdscr.addstr(height - 2, (width - len(self.instructions)) // 2, self.instructions)
