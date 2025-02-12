import pandas as pd
import spacy
import os
from collections import defaultdict
from pathlib import Path

# Load English NLP model
nlp = spacy.load("en_core_web_sm")


def generate_word_forms(word):
    """Generate different forms of a word using NLP."""
    doc = nlp(word)
    forms = {word}
    for token in doc:
        forms.add(token.lemma_)  # Add lemma (base form)
        forms.add(token.text)  # Original text
        forms.add(token.lower_)  # Lowercase form
    return forms


def load_stance_markers(csv_path):
    """Load stance markers from a CSV and generate all word forms."""
    df = pd.read_csv(csv_path)
    stance_dict = defaultdict(set)

    for _, row in df.iterrows():
        stance_type = row["Construction Type"].strip()
        markers = row["Markers"].split(", ")

        for marker in markers:
            stance_dict[stance_type].update(generate_word_forms(marker))

    return stance_dict


def count_stance_markers(text_path, stance_dict):
    """Count the frequency of stance markers in a given text file."""
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read().lower()

    stance_counts = {stance: 0 for stance in stance_dict}

    for stance, markers in stance_dict.items():
        for marker in markers:
            stance_counts[stance] += text.count(marker)

    return stance_counts


def save_results(output_path, stance_counts):
    """Save the stance marker frequencies to a CSV file."""
    df = pd.DataFrame(list(stance_counts.items()), columns=["Construction Type", "Frequency"])
    stance_types = ["Attitudinal stance", "", "", "", "", "", "", "", "Epistemic stance", "", "", "", "", "", "", "", "", "Modality","", "", "",]
    df.insert(0, "Stance Type", stance_types[:len(df)])
    df.to_csv(output_path, index=False)

def process_txt(text_file):
    output_csv = text_file[:-4] + '.csv'

    # UPDATE!!!!!
    stance_csv = "/Users/caotony/PycharmProjects/csg_thesis/stage2_data_processing/List_of_stance_markers.csv"  # Update this if needed
    # Load stance markers
    stance_dict = load_stance_markers(stance_csv)

    # Count frequencies
    stance_counts = count_stance_markers(text_file, stance_dict)

    # Save results
    save_results(output_csv, stance_counts)

    print(f"Stance marker frequencies saved to: {output_csv}")

if __name__ == "__main__":
    # Define file paths
    stance_csv = "/Users/caotony/PycharmProjects/csg_thesis/stage2_data_processing/valid_marker.csv"  # Update this if needed
    text_file_folder = "/Users/caotony/PycharmProjects/csg_thesis/stage2_data_processing/"
    fnames = ['2021.txt','2022.txt','2023.txt']
    for fname in fnames:
        txt = text_file_folder + 'fname'
        process_txt(fname)

