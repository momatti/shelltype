"""
Results module - handles display of basic typing test results
"""

from _curses import window

# Import custom modules
from .header import ResultsHeader
from .instructions import ResultInstructions
from .stats import ResultStats

class ResultsInterface:
    """Shows the basic results screen."""

    def __init__(self, typing_session, stdscr: window):
        self.stdscr = stdscr
        self.typing_session = typing_session

    def draw(self):
        self.stdscr.clear()

        ResultsHeader(self.typing_session, self.stdscr).draw()
        ResultStats(self.typing_session, self.stdscr).draw()
        ResultInstructions(self.stdscr).draw()

        self.stdscr.refresh()
        self.watch_user_input()

    def watch_user_input(self):
        """Wait for user input to exit or continue."""
        while True:
            key = self.stdscr.getch()
            if key == 27:
                return key  # Exit on ESC (27)
            elif key == 10: # Enter key
                return key
