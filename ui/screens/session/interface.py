"""
Interface module - handles the UI for the typing test itself
"""

from _curses import window

# Import custom modules
from  ui.screens.session.header import SessionHeader
from  ui.screens.session.input import SessionInput
from  ui.screens.session.instructions import SessionInstructions
from  ui.screens.session. progress_bar import SessionProgressBar
from  ui.screens.session.word_current import SessionCurrentWord
from  ui.screens.session.words import SessionWords

class SessionInterface:
    """Draws the typing session interface."""

    def __init__(self, typing_session, stdscr: window ):
        self.typing_session = typing_session
        self.stdscr = stdscr

    def draw(self):
        self.stdscr.clear()

        # Draw each interface component
        SessionHeader(self.typing_session, self.stdscr).draw()
        SessionProgressBar(self.typing_session, self.stdscr).draw()
        SessionWords(self.typing_session, self.stdscr).draw()
        SessionInput(self.typing_session, self.stdscr).draw()
        SessionCurrentWord(self.typing_session, self.stdscr).draw()
        SessionInstructions(self.stdscr).draw()

        self.stdscr.refresh()
