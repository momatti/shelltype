from _curses import window

import curses
import time

# Import custom modules
from ui.screens.results.interface import ResultsInterface
from ui.screens.session.interface import SessionInterface

from .typing_session import TypingSession

def run_typing_session(stdscr: window, time_limit=60, word_source="common"):
    """Run the typing session."""

    typing_session = TypingSession(time_limit, word_source)
    typing_session.start()

    curses.curs_set(0)  # Hide cursor

    while not typing_session.completed:
        try:
            # Draw interface
            SessionInterface(typing_session, stdscr).draw()

            # Get input
            key = stdscr.getch()
            if key != -1:  # -1 means no key pressed
                typing_session.process_key(key)

            # Update stats
            typing_session.update_stats()

            # Check time limit
            if typing_session.elapsed_time >= typing_session.time_limit:
                typing_session.completed = True

            # Short sleep to reduce CPU usage
            time.sleep(0.01)

        except KeyboardInterrupt:
            typing_session.completed = True

    # Save results
    typing_session.save_result()

    # Show results
    results = ResultsInterface(typing_session, stdscr)
    restart = results.watch_user_input()
    results.draw()

    stdscr.nodelay(False)  # Make getch blocking again

    if restart == 10:
        # Restart the session
        stdscr.clear()
        stdscr.refresh()
        run_typing_session(stdscr, time_limit, word_source)
