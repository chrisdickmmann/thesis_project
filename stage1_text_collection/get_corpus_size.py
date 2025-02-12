import os
import csv
import nltk
from nltk.tokenize import word_tokenize

# Ensure you have the necessary tokenizer
nltk.download('punkt')


def count_tokens_in_folder(folder_path, output_csv):
    data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                tokens = word_tokenize(text)
                token_count = len(tokens)
                data.append([filename, token_count])

    # Save results to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Token Count"])
        writer.writerows(data)

    print(f"Token counts saved to {output_csv}")


# Example usage
folder_path = "/Users/caotony/PycharmProjects/csg_thesis/stage1_text_collection/textex"  # Change this to your folder path
output_csv = "token_counts.csv"
count_tokens_in_folder(folder_path, output_csv)
