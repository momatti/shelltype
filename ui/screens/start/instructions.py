from _curses import window

class StartInstructions:
    """Intructions for the start menu."""
    def __init__(self, stdscr: window):
        self.stdscr = stdscr
        self.width, self.height = stdscr.getmaxyx()

        self.footer = "↑↓ to navigate | ENTER to select"

    def draw(self):
        if (self.width - len(self.footer)) // 2 > 0 and self.height - 3 > 0:
            self.stdscr.addstr(self.height - 3, (self.width - len(self.footer)) // 2, self.footer)
