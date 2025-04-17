from _curses import window

# Import custom modules
from ui.charts import draw_bar_chart, draw_line_chart

class AnalyticsInterface:
    """Shows the detailed analytics screen."""

    def __init__(self, stdscr: window, typing_test):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Prepare analytics data
        analytics_title = "DETAILED TYPING ANALYTICS"
        stdscr.addstr(1, (width - len(analytics_title)) // 2, analytics_title)

        # Calculate advanced metrics
        wpm_over_time = []
        if len(typing_test.word_times) > 0:
            # Calculate WPM for each word
            for i, word_time in enumerate(typing_test.word_times):
                if word_time > 0:
                    word = typing_test.words[i]
                    wpm = (len(word) / 5) / (word_time / 60)
                    wpm_over_time.append(wpm)

        # Key performance data
        key_data = []
        for key, count in sorted(typing_test.key_frequency.items(), key=lambda x: x[1], reverse=True)[:5]:
            if len(key) == 1 and key.isprintable():
                key_data.append((key, count))

        # Mistake data
        mistake_data = []
        for char, count in sorted(typing_test.mistakes_by_char.items(), key=lambda x: x[1], reverse=True)[:5]:
            mistake_data.append((char, count))

        # Performance metrics
        metrics = [
            ("WPM", round(typing_test.wpm, 1)),
            ("Accuracy", f"{round(typing_test.accuracy, 1)}%"),
            ("Consistency", f"{round(typing_test.consistency, 1)}%"),
            ("Burst Speed", f"{round(typing_test.get_burst_speed(), 1)} WPM"),
            ("Backspaces", typing_test.backspaces)
        ]

        # Calculate sections
        left_section_width = width // 2 - 5
        right_section_width = width // 2 - 5

        # Draw sections
        section_y = 3

        # Draw metrics section
        stdscr.addstr(section_y, 2, "PERFORMANCE METRICS")
        section_y += 1

        for i, (metric, value) in enumerate(metrics):
            display = f"{metric}: {value}"
            stdscr.addstr(section_y + i, 4, display)

        section_y += len(metrics) + 2

        # Draw WPM over time chart if we have data
        if wpm_over_time:
            chart_height = min(10, height - section_y - 10)
            draw_line_chart(stdscr, section_y, 4, left_section_width, chart_height,
                            wpm_over_time, "WPM OVER TIME")
            section_y += chart_height + 2

        # Reset for right column
        section_y = 3
        right_x = left_section_width + 10

        # Draw top keys
        if key_data:
            stdscr.addstr(section_y, right_x, "MOST USED KEYS")
            section_y += 1
            max_key_count = max([count for _, count in key_data])
            draw_bar_chart(stdscr, section_y, right_x, right_section_width, 7,
                        key_data, max_key_count)
            section_y += len(key_data) + 2

        # Draw mistake data
        if mistake_data:
            stdscr.addstr(section_y, right_x, "MOST COMMON MISTAKES")
            section_y += 1
            max_mistake_count = max([count for _, count in mistake_data])
            draw_bar_chart(stdscr, section_y, right_x, right_section_width, 7,
                        mistake_data, max_mistake_count)
            section_y += len(mistake_data) + 2

        # Print additional insights
        insights = []

        # Slowest key insight
        slowest_key = typing_test.get_slowest_key()
        if slowest_key != "Not enough data":
            insights.append(f"Your slowest key is '{slowest_key}'")

        # Consistency insight
        if typing_test.consistency > 0:
            if typing_test.consistency > 80:
                insights.append("Your typing rhythm is very consistent")
            elif typing_test.consistency > 60:
                insights.append("Your typing has good consistency")
            else:
                insights.append("Try to develop a more consistent typing rhythm")

        # Backspace insight
        if typing_test.backspaces > 0:
            backspace_ratio = typing_test.backspaces / (typing_test.correct_chars + typing_test.incorrect_chars)
            if backspace_ratio > 0.2:
                insights.append("You're using backspace frequently - focus on accuracy")
            elif backspace_ratio < 0.05 and typing_test.accuracy < 90:
                insights.append("Try using backspace more to correct mistakes")

        # Draw insights
        if insights:
            stdscr.addstr(height - 7, 4, "INSIGHTS:")
            for i, insight in enumerate(insights[:3]):  # Show max 3 insights
                stdscr.addstr(height - 6 + i, 6, f"• {insight}")

        # Draw footer
        footer = "Press any key to return to main menu..."
        stdscr.addstr(height - 2, (width - len(footer)) // 2, footer)

        stdscr.refresh()
        stdscr.getch()
