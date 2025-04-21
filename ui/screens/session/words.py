from _curses import window


class SessionWords:
    """Draws the words to be typed in the current typing session."""

    def __init__(self, typing_session, window: window):
        self.window = window
        self.width = self.window.getmaxyx()[1]

        self.words_display = ""
        max_display_words = 10
        start_word_idx = max(0, typing_session.current_word_index - 2)
        display_words = typing_session.words[start_word_idx:
                                             start_word_idx + max_display_words]

        for i, word in enumerate(display_words):
            absolute_idx = start_word_idx + i
            if absolute_idx == typing_session.current_word_index:
                self.words_display += f" [{word}] "
            else:
                self.words_display += f" {word} "

    def draw(self):
        self.window.addstr(6, (self.width - len(self.words_display)
                               ) // 2, self.words_display[:self.width-1])
