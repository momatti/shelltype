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
    parser.add_argument('--menu', action='store_true',
                        help='Show the main menu (default behavior)')
    args = parser.parse_args()

    def initialize_curses(stdscr: window):
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)  # Hide cursor

        stdscr.erase()

        if args.menu:
            StartInterface(stdscr)
        else:
            run_typing_session(stdscr, args.time, args.words)

    try:
        curses.wrapper(initialize_curses)
    except KeyboardInterrupt:
        print("Typing session terminated.")

if __name__ == "__main__":
    main()
