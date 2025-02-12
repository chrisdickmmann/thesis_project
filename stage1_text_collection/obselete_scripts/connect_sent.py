import os


def replace_newlines_in_files(input_dir, output_dir):
    """
    Reads all .txt files in the input directory, replaces all newlines with spaces,
    and saves the modified files to the output directory.

    Parameters:
    input_dir (str): Directory containing the original text files.
    output_dir (str): Directory where the modified files will be saved.
    """
    # Ensure the output directory exists, create if not
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, filename)

            # Read the file content
            with open(input_file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Replace all newline characters with a space
            modified_content = content.replace('\n', ' ')

            # Write the modified content to the output directory
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)

            print(f"Processed: {filename}")


# Example usage:
input_directory = '/Users/caotony/PycharmProjects/csg_thesis/rough_sentence_token'  # Replace with the path to the input directory
output_directory = '/Users/caotony/PycharmProjects/csg_thesis/rough_text'  # Replace with the path to the output directory

replace_newlines_in_files(input_directory, output_directory)
