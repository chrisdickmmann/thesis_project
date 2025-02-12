import re
import csv
import os
import nltk
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Ensure that necessary NLTK resources are downloaded
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')  # Add this line to download the missing resource

# Input and output folder paths
input_folder = "textex"         # Replace with the folder containing your corpus files
markers_file = "Rmarkers.txt"  # Replace with your stance markers file path
output_folder = "stance_sum"     # Folder for saving output files

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Read stance markers from file
with open(markers_file, "r", encoding="utf-8") as mf:
    markers = [line.strip().lower() for line in mf]  # Convert markers to lowercase

# Create a regex pattern for all markers
regex_pattern = r"\b(" + "|".join(re.escape(marker) for marker in markers) + r")\b"

# Function to lemmatize a word (convert it to its root form)
def lemmatize_word(word):
    return lemmatizer.lemmatize(word.lower())

# Process all text files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):  # Process only .txt files
        input_file_path = os.path.join(input_folder, filename)
        output_file_name = f"{os.path.splitext(filename)[0]}.csv"
        output_file_path = os.path.join(output_folder, output_file_name)

        # Read the corpus and count frequencies
        frequencies = Counter()

        with open(input_file_path, "r", encoding="utf-8") as cf:
            for line in cf:
                # Tokenize the line and process each token (word)
                tokens = word_tokenize(line)
                for token in tokens:
                    # If the token matches a stance marker (after lemmatization), count it
                    if re.search(regex_pattern, token, flags=re.IGNORECASE):
                        root_form = lemmatize_word(token)
                        if root_form in markers:  # Only count if the root form is a marker
                            frequencies[root_form] += 1

        # Sort the frequencies in descending order
        sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

        # Write the frequencies to the output CSV
        with open(output_file_path, "w", encoding="utf-8", newline="") as of:
            writer = csv.writer(of)
            writer.writerow(["Marker", "Frequency"])  # Write header
            for marker, count in sorted_frequencies:
                writer.writerow([marker, count])

        print(f"Processed {filename} -> {output_file_path}")

print(f"All files processed. Results saved in {output_folder}")