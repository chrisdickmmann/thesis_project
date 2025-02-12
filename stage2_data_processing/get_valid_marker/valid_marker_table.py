import pandas as pd

# Load the valid marker data
df = pd.read_csv("/Users/caotony/PycharmProjects/csg_thesis/stage2_data_processing/get_valid_marker/valid_marker.csv")

# Create a dictionary with unique construction types as keys and empty strings as values
construction_dict = {ctype: "" for ctype in df["Construction Type"].unique()}
stance_dict = {}

# Populate the dictionary with markers and stance types
for ctype in construction_dict:
    markers = df[df["Construction Type"] == ctype]["Marker"]
    construction_dict[ctype] = ", ".join(markers)
    stance_type = df[df["Construction Type"] == ctype]["Stance Type"].unique()
    stance_dict[ctype] = stance_type[0] if len(stance_type) > 0 else "Unknown"

# Convert dictionaries to DataFrame
df_construction = pd.DataFrame(list(construction_dict.items()), columns=["Construction Type", "Markers"])
df_construction.insert(0, "Stance Type", df_construction["Construction Type"].map(stance_dict))

# Sort by Stance Type first, then by Construction Type
df_construction = df_construction.sort_values(by=["Stance Type", "Construction Type"], ascending=[True, True])

# Save as CSV
df_construction.to_csv("valid_marker_table.csv", index=False)

print("Valid marker table saved as valid_marker_table.csv.")
