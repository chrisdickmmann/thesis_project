import pandas as pd
import re
import os
import spacy
import pyinflect

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


def get_verb_forms(word):
    doc = nlp(word)
    if doc[0].pos_ == "VERB":
        return [
            doc[0]._.inflect("VBG"),  # Present participle
            doc[0]._.inflect("VBD"),  # Past tense
            doc[0]._.inflect("VBZ"),  # Third-person singular
            doc[0]._.inflect("VBN")  # Past participle
        ]
    return []


def extract_sentences_from_files(folder_path, marker_file):
    # Read marker file and extract Marker column as list
    print(f"Loading marker file: {marker_file}")
    df_markers = pd.read_csv(marker_file)
    markers = df_markers.iloc[:, 0].dropna().tolist()
    print(f"Found {len(markers)} markers.")


    # Use a set to track unique markers with verb forms already inserted
    processed_markers = set()


    new_markers = []

    for marker in markers:
        if marker not in processed_markers:  # Check if this marker has been processed
            verb_forms = get_verb_forms(marker)
            if verb_forms:
                # Add the marker itself first, then add its verb forms
                new_markers.append(marker)
                for form in verb_forms:
                    new_markers.append(form)  # Insert each verb form separately
                print("insert " + str(len(verb_forms)) + " variations for " + str(marker))
                processed_markers.add(marker)  # Mark this marker as processed
            else:
                new_markers.append(marker)  # Add the original marker if no verb forms
        else:
            new_markers.append(marker)  # If already processed, just add it

    file_paths = [os.path.abspath(os.path.join(folder_path, f)) for f in os.listdir(folder_path)]
    print(f"Found {len(file_paths)} files in {folder_path}.")

    folder_name = folder_path[-4:]

    all_sentences = []

    # Iterate over each file path
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        # Read file line by line
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        print(f"Processing file: {file_path} with {len(lines)} lines.")

        # Process each marker
        for marker in markers:
            marker_sentences = [line for line in lines if re.search(rf'\b{re.escape(marker)}\b', line)]
            print(f"Found {len(marker_sentences)} sentences with marker: {marker}")

            for sentence in marker_sentences:
                # append dictionary to list
                all_sentences.append({'IsStance': None, 'marker': marker, 'sentence': sentence})

    # Save all collected sentences to a single CSV file
    if all_sentences:
        # save list to dataframe
        df_output = pd.DataFrame(all_sentences)
        # Sort DataFrame by 'marker' in ascending order
        df_output = df_output.sort_values(by="marker", ascending=True)

        output_filename = folder_name + ".csv"
        df_output.to_csv(output_filename, index=False, encoding='utf-8')
        print(f"Saved: {output_filename}")
    else:
        print(f"No sentences found for {folder_name}.")


if __name__ == "__main__":
    for i in ['2021', '2022', '2023']:
        folder_path = f"/Users/caotony/PycharmProjects/csg_thesis/stage1_text_collection/text_sentence_grouped/{i}"
        marker_file_path = "/Users/caotony/PycharmProjects/csg_thesis/stage2_data_processing/valid_marker.csv"  # Provided CSV file

        print(f"Starting extraction for year {i}...")
        extract_sentences_from_files(folder_path, marker_file_path)
        print(f"Finished extraction for year {i}.\n")
