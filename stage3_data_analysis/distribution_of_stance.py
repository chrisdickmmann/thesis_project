import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file (replace with your file path)
df = pd.read_csv('/Users/caotony/PycharmProjects/csg_thesis/stage3_data_analysis/marker_fre_total.csv')

# Group by 'year' and 'stance_type' and count the markers
df_grouped = df.groupby(['year of release', 'stance_type']).size().reset_index(name='marker_count')

# Calculate the total markers per year
df_total_per_year = df.groupby('year of release').size().reset_index(name='total_count')

# Merge total counts back to the grouped data
df_grouped = pd.merge(df_grouped, df_total_per_year, on='year')

# Normalize the marker counts by dividing by total markers per year and multiplying by 1 million
df_grouped['markers_per_million'] = (df_grouped['marker_count'] / df_grouped['total_count']) * 1_000_000

# Plot the data
plt.figure(figsize=(12, 6))

# Use Seaborn's barplot to compare stance types per million
sns.barplot(data=df_grouped, x='stance_type', y='markers_per_million', hue='year')

# Add labels and title
plt.title('Comparison of Stance Types per Million by Year')
plt.xlabel('Stance Type')
plt.ylabel('Markers per Million')
plt.legend(title='Year')

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
