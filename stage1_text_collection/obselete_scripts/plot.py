import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

# 过滤掉 .DS_Store 文件
file = [file for file in os.listdir("../stance_sum") if not file.startswith('.DS_')]

def read_data_from_file(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            print(f"Reading line: {line}")
            try:
                marker, frequency = line.strip().split(',')
                data[marker] = frequency
            except ValueError:
                print(f"Failed to parse line: {line}")
                # Skip the line if it can't be split into two parts
                continue
        if "Marker" in data:
            del data["Marker"]  # Remove the header if present
    print(f"Data read from {file_path}: {data}")
    return data


def read_data_from_file(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            try:
                marker, frequency = line.strip().split(',')
                data[marker] = frequency
            except ValueError:
                # Skip the line if it can't be split into two parts
                continue
        if "Marker" in data:
            del data["Marker"]  # Remove the header if present
    return data

def plot_top_x_markers(data, file_path="placeholder", title_placeholder="Top 5 Markers and Their Frequencies"):
    # Sort the data by frequency in descending order
    sorted_data = sorted(data.items(), key=lambda item: int(item[1]), reverse=True)
    # Get the top 5 markers and their frequencies
    top_x_markers = [marker for marker, _ in sorted_data[:5][::-1]]
    top_x_frequencies = [int(freq) for _, freq in sorted_data[:5][::-1]]

    # Check if the data is empty
    if not top_x_markers or not top_x_frequencies:
        print(f"No valid data for {title_placeholder}, skipping plot.")
        return

    # Create a DataFrame for seaborn
    df = pd.DataFrame({
        'Markers': top_x_markers,
        'Frequency': top_x_frequencies
    })

    # Create a bar plot using seaborn
    sns.barplot(x='Markers', y='Frequency', data=df)

    # Add labels and title
    plt.xlabel('Markers')
    plt.ylabel('Frequency')
    plt.title(title_placeholder)

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Save the plot
    plt.savefig(file_path, bbox_inches='tight')

    # Close the plot to free up memory
    plt.close()

if __name__ == "__main__":
    for i in file:
        file_path = "./stance_sum/" + i
        obj_path = "./graph/" + i[0:-4]
        data = read_data_from_file(file_path)
        plot_top_x_markers(data, file_path=obj_path, title_placeholder=str(i)[0:-4])