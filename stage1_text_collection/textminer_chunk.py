import os
from PyPDF2 import PdfReader
import re
from nltk.corpus import words

# NLTK's valid words set
valid_words = set(words.words())


def add_space_after_numbers(sentence):
    pattern = r'(\d+)([a-zA-Z])(?!(st|nd|rd|th))'
    result = re.sub(pattern, r'\1 \2', sentence)
    return result


def add_space_before_numbers(sentence):
    pattern = r'([a-zA-Z])(\d+)'
    result = re.sub(pattern, r'\1 \2', sentence)
    return result


def add_apostrophe_to_plural_possessive(text):
    """
    This function detects the pattern of "[word] s" where 's' is isolated
    (followed by a word boundary) in the given text and adds an apostrophe
    between the word and the 's' to form a possessive. It checks if the [word]
    before 's' is a valid word. If not, it returns the original pattern "[word] s".

    Args:
        text (str): The input text that may contain the "[word] s" pattern.

    Returns:
        str: The text with the appropriate apostrophes added for valid patterns
             or the original "[word] s" for invalid ones.
    """
    pattern = re.compile(r'(\b[a-zA-Z]+) s(\b|[.,?!])')

    def replace_callback(match):
        word = match.group(1)
        if word.lower() in valid_words:
            return f"{word}'s{match.group(2)}"
        return f"{word} s{match.group(2)}"

    result = re.sub(pattern, replace_callback, text)
    return result


def merge_contractions(input_text):
    """
    Function to identify and merge the pattern of "[word] 's" in a string.

    Args:
        input_text (str): The string containing potential split "[word] 's" patterns.

    Returns:
        str: The string with the "[word] 's" patterns merged.
    """
    pattern = re.compile(r'(\b[a-zA-Z]+) \'s')

    def merge_match(match):
        return match.group(1) + "'s"

    merged_text = re.sub(pattern, merge_match, input_text)
    return merged_text


def fix_split_words(input_text):
    """
    Function to detect concatenated words in a string (e.g., 'TrainingEmployees') and split them if they form
    two valid words in the dictionary. Other potential split words are merged if they form a valid word.

    Args:
        input_text (str): The string containing potential split or concatenated words.

    Returns:
        str: The string with split words fixed or concatenated properly.
    """

    # A regex pattern to find likely concatenated words: words with no space between them,
    # We'll look for capital letters (as potential word boundaries) following a lowercase word
    pattern = re.compile(r'([a-z]+)([A-Z][a-z]+)')
    '''
    # Function to check and split concatenated words if both parts are valid
    def fix_match(match):
        first_word = match.group(1)
        second_word = match.group(2)

        # Check if both parts are valid words in the dictionary
        if first_word.lower() in valid_words and second_word.lower() in valid_words:
            return first_word + ' ' + second_word  # Split into two valid words
        else:
            return match.group(0)  # Keep the concatenated word as is
    '''
    def fix_match(match):
        first_word = match.group(1)
        second_word = match.group(2)
        return first_word + ' ' + second_word  # Split into two valid words

    # Apply the regex to the input text to fix concatenated words
    fixed_text = re.sub(pattern, fix_match, input_text)

    return fixed_text


def merge_split_words(input_text):
    """
    Function to detect potential split words in a string and merge them if they form a valid word.
    Uses NLTK's word corpus as the dictionary to check for valid merged words.

    Args:
        input_text (str): The string containing potential split words.

    Returns:
        str: The string with split words merged, if valid.
    """

    # A regex pattern to find potential split words: two words separated by a space
    pattern = re.compile(r'(\b[a-zA-Z]+) (\b[a-zA-Z]+)')

    # Function to merge split words if they exist in the dictionary
    def merge_match(match):
        # Merge the two parts into one word
        merged_word = match.group(1) + match.group(2)
        # Check if the merged word is valid in the dictionary
        if merged_word.lower() in valid_words:
            return merged_word  # Merge if valid
        else:
            return match.group(1) + ' ' + match.group(2)  # Keep as separate words if not valid

    # Apply the regex to the input text to merge split words
    merged_text = re.sub(pattern, merge_match, input_text)

    return merged_text


def getlist():
    source_path = "./origin"
    origin_lst = [item for item in os.listdir(source_path) if item[-4:] == ".pdf"]
    return origin_lst


def clean_text(text):
    text = re.sub(r"[^a-zA-Z0-9\s.,;!?&\-'()]", " ", text)
    # Step 1: Remove extra spaces
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space

    # Step 2: Connect split sentences
    # Remove line breaks and hyphens that split words
    text = re.sub(r"-\n", "", text)  # Handle hyphenated words split across lines

    # Step 3: Fix punctuation and spacing
    text = re.sub(r"\s+([.,;!?])", r"\1", text)  # Remove spaces before punctuation
    text = re.sub(r"([.,;!?])(\w)", r"\1 \2", text)  # Add space after punctuation
    # text = re.sub(r'(\d)-\s*(\d)', r'\1-\2', text)  # Preserve hyphen between numbers
    # text = re.sub(r'(\w)-\s*(\w)', r'\1\2', text)  # Replace hyphen between non-numeric words

    text = text.strip()
    return text


def save_txt(content, path):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def pdf2txt(fname):
    inpath = "/Users/caotony/PycharmProjects/csg_thesis/origin/" + fname
    outpath = "/Users/caotony/PycharmProjects/csg_thesis/textex/" + fname[:-4] + ".txt"

    reader = PdfReader(inpath)

    extracted = ''
    for page in reader.pages:
        pagetext = page.extract_text()  # one string for every page
        extracted += clean_text(pagetext) + "\n"
        extracted = merge_contractions(extracted)
        extracted = add_apostrophe_to_plural_possessive(extracted)
        extracted = add_space_after_numbers(extracted)
        extracted = add_space_before_numbers(extracted)
        extracted = merge_split_words(extracted)
        extracted = fix_split_words(extracted)

    save_txt(extracted, outpath)
    print("file:" + fname + " processed")


def main():
    lst = getlist()
    for file in lst:
        pdf2txt(file)


main()
