"""
This module defines color constants.
Make sure to update this if you change the color scheme in the main.py.
"""

from curses import color_pair

CURRENT_CHARACTER = color_pair(1)
CORRECT_CHARACTER = color_pair(2)
INCORRECT_CHARACTER = color_pair(3)
