""" Line chart for typing speed over time."""

from _curses import window

import curses

def draw_line_chart(stdscr: window, y, x, width, height, values, title=""):
    if not values or width <= 20:
        return

    # Draw title
    if title:
        stdscr.addstr(y, x, title)
        y += 1

    # Calculate dimensions
    plot_width = width - 10
    plot_height = height - 2

    if plot_width <= 0 or plot_height <= 0 or len(values) <= 1:
        return

    # Get min and max values
    min_val = min(values)
    max_val = max(values)
    value_range = max_val - min_val if max_val > min_val else 1

    # Draw axes
    for i in range(plot_height):
        stdscr.addstr(y + i, x, "|")

    for i in range(plot_width):
        stdscr.addstr(y + plot_height, x + i + 1, "-")

    # Draw scale
    stdscr.addstr(y, x - 4, f"{max_val:.0f}")
    stdscr.addstr(y + plot_height - 1, x - 4, f"{min_val:.0f}")

    # Draw line chart
    if len(values) > 1:
        x_step = plot_width / (len(values) - 1)
        prev_x, prev_y = None, None

        for i, value in enumerate(values):
            chart_x = int(x + 1 + i * x_step)
            chart_y = int(y + plot_height - 1 - ((value - min_val) / value_range * (plot_height - 1)))

            if 0 <= chart_y < curses.LINES and 0 <= chart_x < curses.COLS:
                stdscr.addstr(chart_y, chart_x, "●")

                # Draw connecting line
                if prev_x is not None and prev_y is not None:
                    # Simple line drawing
                    if prev_y == chart_y:
                        for x_pos in range(prev_x + 1, chart_x):
                            if x_pos < curses.COLS:
                                stdscr.addstr(chart_y, x_pos, "-")
                    elif prev_x == chart_x:
                        for y_pos in range(min(prev_y, chart_y) + 1, max(prev_y, chart_y)):
                            if y_pos < curses.LINES:
                                stdscr.addstr(y_pos, chart_x, "|")

                prev_x, prev_y = chart_x, chart_y
