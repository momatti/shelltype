"""
Menu module - handles main menu and submenus for the application
"""

from _curses import window

# Importing custom modules
from .instructions import StartInstructions
from .header import StartHeader
from .options import StartOptions

class StartInterface:
    """Shows the main menu."""

    def __init__(self, window: window):
        self.window = window
        self.current_selection = 0

    def draw(self):
        while True:
            self.window.clear()

            StartHeader(self.window).draw()
            StartOptions(self.window).draw()
            StartInstructions(self.window).draw()

            self.window.refresh()
