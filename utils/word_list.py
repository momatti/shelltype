"""
Word list loader module - handles loading and processing word lists
"""

import os
import random

def word_list(word_source="common"):
    """Load the word list based on the selected source."""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    WORD_LISTS = {
        "common": os.path.join(script_dir, "data/word_lists/common.txt"),
        "programming": os.path.join(script_dir, "data/word_lists/programming.txt"),
        "quotes": os.path.join(script_dir, "data/word_lists/quotes.txt")
    }

    try:
        file_path = WORD_LISTS.get(word_source, WORD_LISTS["common"])
        words_dir = os.path.dirname(file_path)

        # Create directory if it doesn't exist
        if not os.path.exists(words_dir):
            os.makedirs(words_dir, exist_ok=True)

        # Create default word lists if they don't exist
        if not os.path.exists(file_path):
            create_default_word_list(file_path, word_source)

        with open(file_path, 'r') as f:
            content = f.read()

        if word_source == "quotes":
            # Split the quotes file into individual quotes
            quotes = [q.strip() for q in content.split('\n\n') if q.strip()]
            # Choose a random quote
            return random.choice(quotes).split()
        else:
            word_list = content.split()
            random.shuffle(word_list)
            return word_list[:100]  # Limit to 100 words

    except Exception as e:
        print(f"Error loading word list: {e}")
        # Fallback to basic words
        return ["the", "be", "to", "of", "and", "a", "in", "that", "have", "I"]

def create_default_word_list(file_path, word_source):
    """Create default word lists for first-time users."""

    default_content = {
        "common": """the be to of and a in that have I it for not on with he as you do at this but his by from they we say her she or an will my one all would there their what so up out if about who get which go me when make can like time no just him know take people into year your good some could them see other than then now look only come its over think also back after use two how our work first well way even new want because any these give day most us""",

        "programming": """algorithm array boolean break case class continue default do else exception extends final finally for function if implements import interface loop method namespace null object oriented package private protected public return static string struct switch syntax try variable void while abstract async await binary branch bug code compile constant debug declare deploy develop document element execute framework function git hardware integer library logic loop machine module null operator parameter program query runtime script source stack structure syntax template token type value version""",

        "quotes": """
            To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.

            The greatest glory in living lies not in never falling, but in rising every time we fall.

            The way to get started is to quit talking and begin doing.

            Your time is limited, so don't waste it living someone else's life.

            If life were predictable it would cease to be life, and be without flavor.

            Life is what happens when you're busy making other plans.

            Spread love everywhere you go. Let no one ever come to you without leaving happier.

            When you reach the end of your rope, tie a knot in it and hang on.

            Always remember that you are absolutely unique. Just like everyone else.

            The future belongs to those who believe in the beauty of their dreams.
        """
    }

    try:
        with open(file_path, 'w') as f:
            f.write(default_content.get(word_source, default_content["common"]))
    except Exception as e:
        print(f"Error creating default word list: {e}")
