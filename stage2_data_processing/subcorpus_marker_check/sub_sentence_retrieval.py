import pandas as pd
import re
import os
import spacy
import pyinflect

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")
def remove_non_alphabet_start(input_string):
    # Check if the first character is not an English alphabet
    if input_string and not input_string[0].isalpha():
        return input_string[1:]  # Remove the first character
    return input_string  # Return the string unchanged if the first character is an alphabet


def get_verb_forms(word):
    doc = nlp(word)
    forms = {
        word,
        doc[0]._.inflect("VBG"),
        doc[0]._.inflect("VBD"),
        doc[0]._.inflect("VBZ"),
        doc[0]._.inflect("VBN")
    }
    # Remove None values from the set
    valid_forms = {form for form in forms if form is not None}
    if valid_forms:
        return list(valid_forms)
    else:
        return [word]


def extract_sentences_from_files(folder_path, marker_file):
    # Read marker file and extract Marker column as list
    print(f"Loading marker file: {marker_file}")
    df_markers = pd.read_csv(marker_file)
    markers_lst = df_markers.iloc[:, 0].dropna().tolist()
    print(f"Found {len(markers_lst)} markers.")


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
        with open(file_path, 'r', encoding='utf-8', errors= 'ignore') as f:
            lines = [line.strip() for line in f if line.strip()]
        print(f"Processing file: {file_path} with {len(lines)} lines.")

        # Process each marker
        for marker in markers_lst:

            def find_stance_and_construction(lookup_value):
                result = df_markers.loc[df_markers['Marker'] == lookup_value, ['Stance Type', 'Construction Type']]
                if not result.empty:
                    return result.iloc[0].tolist()  # Return the first match from column 'B'
                else:
                    return None  # Return None if no match is found

            stance = find_stance_and_construction(marker)[0]
            construction = find_stance_and_construction(marker)[1]


            modality = ['should','must','have to','can','may','could','might','will','shall','would']
            adverbial = [s.strip() for s in 'happily, conveniently, proudly, naturally, inevitably, unfortunately, rightly, incredibly,  always, ' \
            'clearly, never, of course, actually, really, in fact, indeed, always, clearly, never, of course, ' \
            'actually, really, in fact, indeed'.split(',')]
            exception_marker = modality + adverbial

            if str(marker).strip() not in exception_marker:
                marker_sublist = get_verb_forms(marker)
                that_list = list(map(lambda x: x + " that", marker_sublist))
                to_list = list(map(lambda x: x + " to", marker_sublist))
                marker_sublist = that_list + to_list
            else:
                marker_sublist = [str(marker).strip()]

            for submarker in marker_sublist:

                sub_sentences = [line for line in lines if re.search(rf'\b{re.escape(submarker)}\b', line)]

                # print(f"Found {len(marker_sentences)} sentences with marker: {subm}")

                for sentence in sub_sentences:
                    # Wrap the marker in square brackets in the sentence
                    highlighted_sentence = re.sub(rf'\b{re.escape(submarker)}\b', r'[\g<0>]', sentence)
                    highlighted_sentence = remove_non_alphabet_start(highlighted_sentence)


                    # Append a new column 'filename' and 'highlighted_sentence'
                    all_sentences.append({'IsStance': None, 'marker': marker, 'sentence': highlighted_sentence,
                                          'sourcefile': os.path.basename(file_path),
                                         'stance type': stance, 'construction type': construction,})

    # Save all collected sentences to a single CSV file
    if all_sentences:
        df_output = pd.DataFrame(all_sentences)

        # Sort DataFrame by 'marker' in ascending order
        df_output = df_output.sort_values(by="marker", ascending=True)

        # Save to CSV
        output_filename = folder_name + "_with_type" + ".csv"

        output_path = '/Users/caotony/PycharmProjects/csg_thesis/stage2_data_processing/subcorpus_marker_check' \
                     '/manual_check/'

        df_output.to_csv(output_path + output_filename, index=False, encoding='utf-8')
        print(f"Saved: {output_filename}")
    else:
        print(f"No sentences found for {folder_name}.")


if __name__ == "__main__":
    for i in ['2021', '2022', '2023']:
        folder_path = f"/Users/caotony/PycharmProjects/csg_thesis/stage1_text_collection/text_in_sentences/{i}"
        marker_file_path = "/Users/caotony/PycharmProjects/csg_thesis/stage2_data_processing/valid_marker.csv"  # Provided CSV file

        print(f"Starting extraction for year {i}...")
        extract_sentences_from_files(folder_path, marker_file_path)
        print(f"Finished extraction for year {i}.\n")