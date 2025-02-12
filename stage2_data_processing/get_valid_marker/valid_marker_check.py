import pandas as pd
import os
import re
from collections import Counter

# Load the list of stance markers
df_markers = pd.read_csv(
    "/Users/caotony/PycharmProjects/csg_thesis/stage2_data_processing/get_valid_marker/(used)Fuoli_markers.csv")

# Placeholder for text file path (update as needed)
text_file_path = "/Users/caotony/PycharmProjects/csg_thesis/stage2_data_processing/get_txt/all_cor_21-23.txt"


# Read the text file
if os.path.exists(text_file_path):
    with open(text_file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()  # Convert to lowercase for case-insensitive matching
else:
    print("Text file not found. Please update the path.")
    text = ""

# Extract markers from "Markers" column
df_markers["Markers"] = df_markers["Markers"].astype(str)
marker_list = list(
    set(marker.strip().lower() for sublist in df_markers["Markers"].str.split(',') for marker in sublist))

# Create stance type and construction type dictionaries
stance_dict = {}
construction_dict = {}

for _, row in df_markers.iterrows():
    markers = [m.strip().lower() for m in row["Markers"].split(',')]
    stance_type = row["Stance Type"]
    construction_type = row["Construction Type"]

    for marker in markers:
        stance_dict[marker] = stance_type
        construction_dict[marker] = construction_type

# Count marker frequency in the text using regex for exact word matches
marker_counts = Counter()
for marker in marker_list:
    pattern = r'(?<!\w)' + re.escape(marker) + r'(?!\w)'
    marker_counts[marker] = len(re.findall(pattern, text, flags=re.IGNORECASE))

# Create result DataFrame
df_results = pd.DataFrame(marker_counts.items(), columns=["Marker", "Frequency"])

# Remove rows where frequency is 0
df_results = df_results[df_results["Frequency"] > 0]

# Define functions for stance and construction type lookup
def get_stance_type(marker):
    return stance_dict.get(marker.lower(), "Unknown")


def get_construction_type(marker):
    return construction_dict.get(marker.lower(), "Unknown")


# Apply functions
df_results["Stance Type"] = df_results["Marker"].apply(get_stance_type)
df_results["Construction Type"] = df_results["Marker"].apply(get_construction_type)

# Sort by frequency
df_results = df_results.sort_values(by="Frequency", ascending=False)

# Save to CSV
save_name = "valid_marker.csv"
df_results.to_csv(save_name, index=False)
print(f"Analysis complete. Results saved to {save_name}")
