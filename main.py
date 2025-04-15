
#!/usr/bin/env python3
import curses
import random
import time
import os
import json
import argparse
from datetime import datetime

class TerminalTypingTest:
    def __init__(self, time_limit=60, word_source="common"):
        self.time_limit = time_limit
        self.word_source = word_source
        self.words = []
        self.current_word_index = 0
        self.current_input = ""
        self.correct_chars = 0
        self.incorrect_chars = 0
        self.start_time = 0
        self.elapsed_time = 0
        self.wpm = 0
        self.accuracy = 100.0
        self.completed = False
        self.load_word_list()

    def load_word_list(self):
        """Load the word list based on the selected source."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        word_lists = {
            "common": os.path.join(script_dir, "word_lists/common.txt"),
            "programming": os.path.join(script_dir, "word_lists/programming.txt"),
            "quotes": os.path.join(script_dir, "word_lists/quotes.txt")
        }
        
        try:
            file_path = word_lists.get(self.word_source, word_lists["common"])
            if not os.path.exists(file_path):
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Create a basic word list for first-time users
                with open(file_path, 'w') as f:
                    default_words = "the be to of and a in that have I it for not on with he as you do at this but his by from they we say her she or an will my one all would there their what so up out if about who get which go me when make can like time no just him know take people into year your good some could them see other than then now look only come its over think also back after use two how our work first well way even new want because any these give day most us"
                    f.write(default_words)
            
            with open(file_path, 'r') as f:
                content = f.read()
                
            if self.word_source == "quotes":
                self.words = [content]  # Use the entire quote
            else:
                word_list = content.split()
                random.shuffle(word_list)
                self.words = word_list[:100]  # Limit to 100 words
                
        except Exception as e:
            print(f"Error loading word list: {e}")
            self.words = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "I"]

    def start(self):
        """Initialize the test and start the timer."""
        self.start_time = time.time()
        self.completed = False

    def process_key(self, key):
        """Process a key press during the typing test."""
        if self.completed:
            return

        if key == 27:  # ESC key
            self.completed = True
            return

        if key in (curses.KEY_BACKSPACE, 127, 8):  # Backspace keys
            if self.current_input:
                self.current_input = self.current_input[:-1]
            return

        if key == ord(' '):  # Space key
            current_word = self.words[self.current_word_index]
            if self.current_input == current_word:
                self.correct_chars += len(current_word)
            else:
                # Count correct characters in the word
                for i, (c1, c2) in enumerate(zip(self.current_input, current_word)):
                    if c1 == c2:
                        self.correct_chars += 1
                    else:
                        self.incorrect_chars += 1
                
                # Account for length differences
                diff = abs(len(self.current_input) - len(current_word))
                self.incorrect_chars += diff

            self.current_word_index += 1
            if self.current_word_index >= len(self.words):
                self.completed = True
            
            self.current_input = ""
            return

        # Regular character input
        if 32 <= key <= 126:  # Printable ASCII
            self.current_input += chr(key)

    def update_stats(self):
        """Update WPM and accuracy stats."""
        self.elapsed_time = time.time() - self.start_time
        
        if self.elapsed_time >= self.time_limit:
            self.completed = True

        if self.elapsed_time > 0:
            # WPM calculation (standard 5 chars per word)
            total_chars = self.correct_chars + self.incorrect_chars
            self.wpm = (total_chars / 5) / (self.elapsed_time / 60)
            
            # Accuracy calculation
            if total_chars > 0:
                self.accuracy = (self.correct_chars / total_chars) * 100
            else:
                self.accuracy = 100.0

    def save_result(self):
        """Save the test result to a JSON file."""
        result = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "wpm": round(self.wpm, 2),
            "accuracy": round(self.accuracy, 2),
            "time_limit": self.time_limit,
            "word_source": self.word_source,
            "elapsed_time": round(self.elapsed_time, 2)
        }
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        history_dir = os.path.join(script_dir, "history")
        
        # Create history directory if it doesn't exist
        os.makedirs(history_dir, exist_ok=True)
        
        history_file = os.path.join(history_dir, "typing_history.json")
        
        try:
            # Read existing history
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []
            
            # Append new result and save
            history.append(result)
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            print(f"Error saving results: {e}")

def draw_interface(stdscr, typing_test):
    """Draw the typing test interface."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    # Draw header
    header = f"Terminal Typing Test | Time: {int(typing_test.time_limit - typing_test.elapsed_time)}s | WPM: {int(typing_test.wpm)} | Accuracy: {int(typing_test.accuracy)}%"
    stdscr.addstr(1, (width - len(header)) // 2, header)
    
    # Draw progress bar
    progress = min(typing_test.elapsed_time / typing_test.time_limit, 1.0)
    bar_width = width - 10
    filled_width = int(bar_width * progress)
    progress_bar = "█" * filled_width + "░" * (bar_width - filled_width)
    stdscr.addstr(3, 5, progress_bar)
    
    # Draw word display (with current word highlighted)
    words_display = ""
    max_display_words = 10
    start_word_idx = max(0, typing_test.current_word_index - 2)
    display_words = typing_test.words[start_word_idx:start_word_idx + max_display_words]
    
    for i, word in enumerate(display_words):
        absolute_idx = start_word_idx + i
        if absolute_idx == typing_test.current_word_index:
            words_display += f" [{word}] "
        else:
            words_display += f" {word} "
    
    stdscr.addstr(6, (width - len(words_display)) // 2, words_display[:width-1])
    
    # Draw current input
    input_display = f"> {typing_test.current_input}"
    stdscr.addstr(9, (width - len(input_display)) // 2, input_display)
    
    # Draw current word for comparison
    if typing_test.current_word_index < len(typing_test.words):
        current_word = typing_test.words[typing_test.current_word_index]
        colored_word = ""
        
        for i, char in enumerate(current_word):
            if i < len(typing_test.current_input):
                if typing_test.current_input[i] == char:
                    # Green for correct characters
                    colored_word += char
                else:
                    # Red for incorrect characters
                    colored_word += char
            else:
                colored_word += char
                
        stdscr.addstr(11, (width - len(current_word)) // 2, colored_word)
    
    # Draw instructions
    instructions = "Press ESC to exit | BACKSPACE to delete | SPACE to submit word"
    stdscr.addstr(height - 2, (width - len(instructions)) // 2, instructions)
    
    stdscr.refresh()

def show_results(stdscr, typing_test):
    """Show the results screen."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    # Calculate stats
    total_chars = typing_test.correct_chars + typing_test.incorrect_chars
    accuracy = typing_test.accuracy
    wpm = typing_test.wpm
    
    # Draw results
    title = "TYPING TEST RESULTS"
    stdscr.addstr(5, (width - len(title)) // 2, title)
    
    result_lines = [
        f"WPM: {int(wpm)}",
        f"Accuracy: {accuracy:.1f}%",
        f"Time: {typing_test.elapsed_time:.1f}s",
        f"Correct characters: {typing_test.correct_chars}",
        f"Incorrect characters: {typing_test.incorrect_chars}",
        f"Total characters: {total_chars}",
        "",
        "Press any key to exit"
    ]
    
    for i, line in enumerate(result_lines):
        stdscr.addstr(7 + i, (width - len(line)) // 2, line)
    
    stdscr.refresh()
    stdscr.getch()

def show_history(stdscr):
    """Show typing history."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    history_file = os.path.join(script_dir, "history/typing_history.json")
    
    if not os.path.exists(history_file):
        stdscr.clear()
        stdscr.addstr(5, 10, "No typing history found.")
        stdscr.addstr(7, 10, "Press any key to continue.")
        stdscr.refresh()
        stdscr.getch()
        return
    
    try:
        with open(history_file, 'r') as f:
            history = json.load(f)
        
        if not history:
            stdscr.clear()
            stdscr.addstr(5, 10, "Typing history is empty.")
            stdscr.addstr(7, 10, "Press any key to continue.")
            stdscr.refresh()
            stdscr.getch()
            return
        
        # Sort by date (newest first)
        history.sort(key=lambda x: x["date"], reverse=True)
        
        current_page = 0
        items_per_page = 10
        total_pages = (len(history) + items_per_page - 1) // items_per_page
        
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            
            title = "TYPING HISTORY"
            stdscr.addstr(1, (width - len(title)) // 2, title)
            
            start_idx = current_page * items_per_page
            end_idx = min(start_idx + items_per_page, len(history))
            page_history = history[start_idx:end_idx]
            
            # Table header
            header = f"{'DATE':<20} {'WPM':<8} {'ACCURACY':<10} {'TIME':<8} {'WORDS':<12}"
            stdscr.addstr(3, 5, header)
            stdscr.addstr(4, 5, "-" * (width - 10))
            
            # Table rows
            for i, entry in enumerate(page_history):
                row = f"{entry['date']:<20} {int(entry['wpm']):<8} {entry['accuracy']:.1f}%{'':<4} {entry['elapsed_time']:.1f}s{'':<3} {entry['word_source']:<12}"
                stdscr.addstr(5 + i, 5, row[:width-10])
            
            # Navigation
            nav_text = f"Page {current_page + 1}/{total_pages} | ← → keys to navigate | Q to exit"
            stdscr.addstr(height - 3, (width - len(nav_text)) // 2, nav_text)
            
            stdscr.refresh()
            
            # Handle keys
            key = stdscr.getch()
            if key in (ord('q'), ord('Q')):
                break
            elif key == curses.KEY_RIGHT and current_page < total_pages - 1:
                current_page += 1
            elif key == curses.KEY_LEFT and current_page > 0:
                current_page -= 1
        
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(5, 10, f"Error loading history: {e}")
        stdscr.addstr(7, 10, "Press any key to continue.")
        stdscr.refresh()
        stdscr.getch()

def main_menu(stdscr):
    """Display the main menu."""
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
        stdscr.addstr(3, (width - len(title)) // 2, title)
        
        # Draw menu items
        for i, item in enumerate(menu_items):
            x = (width - len(item)) // 2
            y = 6 + i * 2
            
            if i == current_selection:
                stdscr.addstr(y, x - 2, "> ")
                stdscr.addstr(y, x, item)
                stdscr.addstr(y, x + len(item) + 1, " <")
            else:
                stdscr.addstr(y, x, item)
        
        # Draw footer
        footer = "↑↓ to navigate | ENTER to select"
        stdscr.addstr(height - 3, (width - len(footer)) // 2, footer)
        
        stdscr.refresh()
        
        # Handle key input
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(menu_items) - 1:
            current_selection += 1
        elif key == 10:  # ENTER key
            if current_selection == 0:
                run_typing_test(stdscr, 30)
            elif current_selection == 1:
                run_typing_test(stdscr, 60)
            elif current_selection == 2:
                run_typing_test(stdscr, 120)
            elif current_selection == 3:
                word_list_menu(stdscr)
            elif current_selection == 4:
                show_history(stdscr)
            elif current_selection == 5:
                break

def word_list_menu(stdscr):
    """Display the word list selection menu."""
    current_selection = 0
    word_lists = [
        ("Common Words", "common"),
        ("Programming Terms", "programming"),
        ("Famous Quotes", "quotes"),
        ("Back to Main Menu", None)
    ]
    
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Draw title
        title = "SELECT WORD LIST"
        stdscr.addstr(3, (width - len(title)) // 2, title)
        
        # Draw menu items
        for i, (item, _) in enumerate(word_lists):
            x = (width - len(item)) // 2
            y = 6 + i * 2
            
            if i == current_selection:
                stdscr.addstr(y, x - 2, "> ")
                stdscr.addstr(y, x, item)
                stdscr.addstr(y, x + len(item) + 1, " <")
            else:
                stdscr.addstr(y, x, item)
        
        # Draw footer
        footer = "↑↓ to navigate | ENTER to select"
        stdscr.addstr(height - 3, (width - len(footer)) // 2, footer)
        
        stdscr.refresh()
        
        # Handle key input
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(word_lists) - 1:
            current_selection += 1
        elif key == 10:  # ENTER key
            selected_option = word_lists[current_selection][1]
            if selected_option is None:
                return
            else:
                run_typing_test(stdscr, 60, selected_option)
                return

def run_typing_test(stdscr, time_limit=60, word_source="common"):
    """Run the typing test."""
    typing_test = TerminalTypingTest(time_limit, word_source)
    typing_test.start()
    
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Make getch non-blocking
    
    while not typing_test.completed:
        try:
            # Draw interface
            draw_interface(stdscr, typing_test)
            
            # Get input
            key = stdscr.getch()
            if key != -1:  # -1 means no key pressed
                typing_test.process_key(key)
            
            # Update stats
            typing_test.update_stats()
            
            # Check time limit
            if typing_test.elapsed_time >= typing_test.time_limit:
                typing_test.completed = True
            
            # Short sleep to reduce CPU usage
            time.sleep(0.01)
            
        except KeyboardInterrupt:
            typing_test.completed = True
    
    # Save results
    typing_test.save_result()
    
    # Show results
    stdscr.nodelay(False)  # Make getch blocking again
    show_results(stdscr, typing_test)

def main():
    parser = argparse.ArgumentParser(description='Terminal Typing Test')
    parser.add_argument('-t', '--time', type=int, default=60,
                        help='Time limit in seconds (default: 60)')
    parser.add_argument('-w', '--words', type=str, default="common",
                        choices=['common', 'programming', 'quotes'],
                        help='Word list to use (default: common)')
    parser.add_argument('--menu', action='store_true',
                        help='Show the main menu (default behavior)')
    args = parser.parse_args()
    
    def initialize_curses(stdscr):
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        
        if args.menu:
            main_menu(stdscr)
        else:
            run_typing_test(stdscr, args.time, args.words)
    
    try:
        curses.wrapper(initialize_curses)
    except KeyboardInterrupt:
        print("Typing test terminated.")

if __name__ == "__main__":
    main()
