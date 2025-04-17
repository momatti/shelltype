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
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Draw each interface component
        SessionHeader(typing_session, stdscr, width).draw()
        SessionProgressBar(typing_session, stdscr, width).draw()
        SessionWords(typing_session, stdscr, width).draw()
        SessionInput(typing_session, stdscr, width).draw()
        SessionCurrentWord(typing_session, stdscr, width).draw()
        SessionInstructions(stdscr, width, height).draw()

        stdscr.refresh()
