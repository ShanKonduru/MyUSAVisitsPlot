import geopandas as gpd
import folium
from folium import plugins
import pandas as pd
import numpy as np

# Replace 'your_file.csv' with the actual name of your CSV file
csv_file = 'FullMyUSAVisit.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file)

# Remove leading and trailing spaces from column names
df.columns = df.columns.str.strip()

# Assuming you have a 'Months' column in your DataFrame
months = df['Months']

# Define conditions and corresponding colors
conditions = [
    (months <= 3),
    (months >= 10),
    (months > 3) & (months < 10)
]

colors = ['red', 'green', 'orange']  # Adjust colors as needed

# Add 'Color' column based on conditions
df['Color'] = np.select(conditions, colors, default='black')

# Print the first few rows of the CSV data
print("CSV Data:")
print(df.head())

# Download the US states shapefile from Natural Earth Data
# You can find the shapefile at: https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-1-states-provinces/
us_states = gpd.read_file('ne_110m_admin_1_states_provinces.shp')

# Remove the 'US-' prefix from the 'iso_3166_2' column in the shapefile
us_states['iso_3166_2'] = us_states['iso_3166_2'].str.replace('US-', '')

# Merge the US states GeoDataFrame with your data based on the 'iso_3166_2' column
merged_data = us_states.merge(df, how='left', left_on='iso_3166_2', right_on='state_abbr')

# Convert 'Days_stayed' column to numeric if it's not already
merged_data['Days_stayed'] = pd.to_numeric(merged_data['Days_stayed'], errors='coerce')

# Print the first few rows of the merged dataset
print("\nMerged Dataset:")
print(merged_data.head())

# Create a Folium map centered around the USA
m = folium.Map(location=[37, -95], zoom_start=4)

# Add a Marker Cluster to the map for better visualization of multiple points
marker_cluster = plugins.MarkerCluster().add_to(m)

# Iterate over each row in the merged data and add markers only for states with data
for index, row in merged_data.iterrows():
    if not pd.isnull(row['Days_stayed']) and row['Days_stayed'] > 0:
        tooltip = f"State: {row['state_abbr']} Total Days Stayed: {row['Days_stayed']}"

        # Add markers to the Marker Cluster
        # Customize the icon color based on the 'Color' column
        folium.Marker(
            location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
            popup=tooltip,
            icon=folium.Icon(color=row['Color'])
        ).add_to(marker_cluster)

# Save the map as an HTML file
m.save('visited_places_map.html')
