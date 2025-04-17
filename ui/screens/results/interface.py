"""
Results module - handles display of basic typing test results
"""

from _curses import window

def ResultsInterface(stdscr: window, typing_session):
    """Shows the basic results screen."""

    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Calculate results
    total_chars = typing_session.correct_chars + typing_session.incorrect_chars
    accuracy = typing_session.accuracy
    wpm = typing_session.wpm

    # Draw results
    title = "TYPING TEST RESULTS"
    stdscr.addstr(5, (width - len(title)) // 2, title)

    result_lines = [
        f"WPM: {int(wpm)}",
        f"Accuracy: {accuracy:.1f}%",
        f"Time: {typing_session.elapsed_time:.1f}s / {typing_session.time_limit}s",
        f"Correct characters: {typing_session.correct_chars}",
        f"Incorrect characters: {typing_session.incorrect_chars}",
        f"Total characters: {total_chars}",
        f"Words completed: {typing_session.current_word_index}",
        "",
        "Press any key to see detailed analytics..."
    ]

    for i, line in enumerate(result_lines):
        y_pos = 7 + i
        if y_pos < height - 1:  # Make sure we don't print outside the screen
            stdscr.addstr(y_pos, (width - len(line)) // 2, line)

    stdscr.refresh()
    stdscr.getch()
