#!/usr/bin/env python3

"""
Terminal Typing Session - A MonkeyType clone for the terminal
Main entry point for the application
"""

from _curses import window

import curses
import argparse

# Import custom modules
from ui.screens.start import StartInterface
from core.session.run_session import run_typing_session


def main():
    """Parse command line arguments and start the application."""
    parser = argparse.ArgumentParser(description='Terminal Typing Test')
    parser.add_argument('-t', '--time', type=int, default=60,
                        help='Time limit in seconds (default: 60)')
    parser.add_argument('-w', '--words', type=str, default="common",
                        choices=['common', 'programming', 'quotes'],
                        help='Word list to use (default: common)')
    parser.add_argument('-m', '--menu', action='store_true',
                        help='Show the main menu (default behavior)')
    args = parser.parse_args()

    def initialize_curses(stdscr: window):
        """Initialize curses and set up color pairs."""
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_YELLOW,
                         curses.COLOR_BLACK)  # CURRENT character
        curses.init_pair(2, curses.COLOR_GREEN,
                         curses.COLOR_BLACK)  # CORRECT character
        # INCORRECT character
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(True)  # Make getch non-blocking

        stdscr.clear() # Start with a clear screen

        if args.menu:
            StartInterface(stdscr).draw()
        else:
            run_typing_session(stdscr, args.time, args.words)

    try:
        curses.wrapper(initialize_curses)
    except KeyboardInterrupt:
        print("Shelltyping session finished.")


if __name__ == "__main__":
    main()
