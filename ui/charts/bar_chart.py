"""Bar chart"""

import curses

def draw_bar_chart(stdscr, y, x, width, values, max_value, title=""):
    if not values:
        return

    # Draw title
    if title:
        stdscr.addstr(y, x, title)
        y += 1

    # Calculate bar width
    bar_width = width - 20  # Leave space for labels

    # Draw each bar
    for i, (label, value) in enumerate(values):
        if y + i >= curses.LINES - 1:
            break

        # Draw label
        stdscr.addstr(y + i, x, f"{label[:15]:<15}")

        # Draw bar
        bar_length = int((value / max_value) * bar_width) if max_value > 0 else 0
        bar = "█" * bar_length
        stdscr.addstr(y + i, x + 15, bar)

        # Draw value
        value_str = f" {value:.1f}" if isinstance(value, float) else f" {value}"
        stdscr.addstr(y + i, x + 15 + bar_length + 1, value_str)

