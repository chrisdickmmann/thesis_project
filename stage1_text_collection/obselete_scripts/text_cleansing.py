from spellchecker import SpellChecker
import os
from tqdm import tqdm
# Get the list of all files in the current directory
files_in_directory = os.listdir()

# Filter out only .txt files
txt_files = [file for file in files_in_directory if file.endswith('.txt')]
def blank_strip(text):
    words = text.split()
    print("Splitting text...")
    wdc = len(words)
    plain_words = []
    for crt_prg, word in tqdm(enumerate(words, 1), total=wdc, desc="Processing words", unit="word"):
            plain_words.append(word)
    plain_text = " ".join(plain_words)
    return plain_text

# Process each .txt file
for txt_file in txt_files:
    try:
        # Open file with a safe encoding (ISO-8859-1 or latin1)
        with open(txt_file, 'r', encoding='ISO-8859-1') as file:
            content = file.read()
            if content:
                print(f"Content read within {txt_file}")

        # Perform spell check
        plain_text = blank_strip(content)

        # Save the corrected content to a new file
        corrected_filename = f"corrected_{txt_file}"
        with open(corrected_filename, 'w', encoding='utf-8') as file:
            file.write(plain_text)

        print(f"Spell check completed. Saved as '{corrected_filename}'.")

    except UnicodeDecodeError as e:
        print(f"Error reading {txt_file}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred with {txt_file}: {e}")
