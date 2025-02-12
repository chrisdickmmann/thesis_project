import os
from pathlib import Path


def merge_texts_in_folder(folder_path):
    """Read all text files in a folder, merge them with blanks, and save as a single file."""
    folder = Path(folder_path)
    parent_folder = folder.parent
    output_file = parent_folder / f"{folder.name}.txt"

    text_contents = []
    for txt_file in sorted(folder.glob("*.txt")):
        with open(txt_file, "r", encoding="utf-8") as f:
            text_contents.append(f.read().strip())

    merged_text = " ".join(text_contents)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(merged_text)

    # Remove all files and subdirectories in the folder
    for item in folder.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            os.rmdir(item)  # Only removes empty subdirectories

    # Ensure folder is empty before removing it
    try:
        folder.rmdir()
        print(f"Merged text saved to: {output_file}")
    except OSError as e:
        print(f"Error: {e}. The directory may not be empty.")


if __name__ == "__main__":
    paths = ['/Users/caotony/PycharmProjects/csg_thesis/stage2_data_processing/2023',
             '/Users/caotony/PycharmProjects/csg_thesis/stage2_data_processing/all_cor_21-23']
    for path in paths:
        merge_texts_in_folder(path)