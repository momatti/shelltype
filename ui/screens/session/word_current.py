from _curses import window

class SessionCurrentWord:
    """Current word display - shows the word being typed in the current session"""

    def __init__(self, typing_session, stdscr: window):
        self.stdscr = stdscr
        self.width = stdscr.getmaxyx()[1]

        self.colored_word = ""

        if typing_session.current_word_index < len(typing_session.words):
            current_word = typing_session.words[typing_session.current_word_index]

            # Get the current input
            for i, char in enumerate(current_word):
                if i < len(typing_session.current_input):
                    if typing_session.current_input[i] == char:
                        # Green for correct characters
                        self.colored_word += char
                    else:
                        # Red for incorrect characters
                        self.colored_word += char
                else:
                    self.colored_word += char

            if len(self.colored_word) > self.width - 2:
                self.colored_word = self.colored_word[:self.width - 5] + "..."

    def draw(self):
        self.stdscr.addstr(11, (self.width - len(self.colored_word)) // 2, self.colored_word)
