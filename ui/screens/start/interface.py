"""
Menu module - handles main menu and submenus for the application
"""

from _curses import window

class StartInterface:
    """Shows the main menu."""

    def __init__(self, stdscr: window):
        current_selection = 0
        menu_items = [
            "Start Typing Test (30s)",
            "Start Typing Test (60s)",
            "Start Typing Test (120s)",
            "Word Lists",
            "View History",
            "Exit"
        ]

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            # Draw title
            title = "TERMINAL TYPING TEST"
            if (width - len(title)) // 2 > 0 and 3 < height:
                stdscr.addstr(3, (width - len(title)) // 2, title)

            # Draw menu items
            for i, item in enumerate(menu_items):
                x = (width - len(item)) // 2
                y = 6 + i * 2

                if y < height - 1 and x > 2:  # Make sure we're within the screen
                    if i == current_selection:
                        stdscr.addstr(y, x - 2, "> ")
                        stdscr.addstr(y, x, item)
                        if x + len(item) + 2 < width:
                            stdscr.addstr(y, x + len(item) + 1, " <")
                    else:
                        stdscr.addstr(y, x, item)

            # Draw footer
            footer = "↑↓ to navigate | ENTER to select"
            if (width - len(footer)) // 2 > 0 and height - 3 > 0:
                stdscr.addstr(height - 3, (width - len(footer)) // 2, footer)

            stdscr.refresh()
