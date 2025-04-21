from _curses import window

class StartOptions:
    def __init__(self, window: window):
        self.window = window
        self.height, self.width = window.getmaxyx()

        self.options = [
            "Start Typing Test (15s)",
            "Start Typing Test (30s)",
            "Start Typing Test (60s)",
            "Start Typing Test (120s)",
            "",
            "Word Lists",
            "View History",
            ""
            "Exit"
        ]

        #  State
        self.current_selection = 0

    def draw(self):
        for i, item in enumerate(self.options):
            x = (self.width - len(item)) // 2
            y = 6 + i * 2

            if y < self.height - 1 and x > 2:  # Make sure we're within the screen
                if i == self.current_selection:
                    self.window.addstr(y, x - 2, "> ")
                    self.window.addstr(y, x, item)
                    if x + len(item) + 2 < self.width:
                        self.window.addstr(y, x + len(item) + 1, " <")
                else:
                    self.window.addstr(y, x, item)
