import geopandas as gpd
import folium
from folium import plugins
import pandas as pd
import numpy as np

class GeoSpatialGraph:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.df = None
        self.us_states = None
        self.merged_data = None
        self.map = None

    def read_csv(self):
        self.df = pd.read_csv(self.csv_file)
        self.df.columns = self.df.columns.str.strip()

    def process_data(self):
        # Remove leading and trailing spaces from column names
        self.df.columns = self.df.columns.str.strip()

        # Assuming you have a 'Months' column in your DataFrame
        months = self.df['Months']

        # Define conditions and corresponding colors
        conditions = [
            (months <= 3),
            (months >= 10),
            (months > 3) & (months < 10)
        ]

        colors = ['red', 'green', 'orange']  # Adjust colors as needed

        # Add 'Color' column based on conditions
        self.df['Color'] = np.select(conditions, colors, default='black')

        # Print the first few rows of the CSV data
        print("CSV Data:")
        print(self.df.head())

        # Download the US states shapefile from Natural Earth Data
        # You can find the shapefile at: https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-1-states-provinces/
        us_states = gpd.read_file('ne_110m_admin_1_states_provinces.shp')

        # Remove the 'US-' prefix from the 'iso_3166_2' column in the shapefile
        us_states['iso_3166_2'] = us_states['iso_3166_2'].str.replace('US-', '')

        # Merge the US states GeoDataFrame with your data based on the 'iso_3166_2' column
        self.merged_data = us_states.merge(self.df, how='left', left_on='iso_3166_2', right_on='state_abbr')

        # Convert 'Days_stayed' column to numeric if it's not already
        self.merged_data['Days_stayed'] = pd.to_numeric(self.merged_data['Days_stayed'], errors='coerce')

        # Print the first few rows of the merged dataset
        print("\nMerged Dataset:")
        print(self.merged_data.head())


    def create_map(self):
        # Create a Folium map centered around the USA
        self.map = folium.Map(location=[37, -95], zoom_start=4)

        # Add a Marker Cluster to the map for better visualization of multiple points
        marker_cluster = plugins.MarkerCluster().add_to(self.map)

        # Iterate over each row in the merged data and add markers only for states with data
        for index, row in self.merged_data.iterrows():
            if not pd.isnull(row['Days_stayed']) and row['Days_stayed'] > 0:
                tooltip = f"State: {row['state_abbr']} Total Days Stayed: {row['Days_stayed']}"

                # Add markers to the Marker Cluster
                # Customize the icon color based on the 'Color' column
                folium.Marker(
                    location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
                    popup=tooltip,
                    icon=folium.Icon(color=row['Color'])
                ).add_to(marker_cluster)

    def save_map_html(self, html_file_path):
        # Save the map as an HTML file
        self.map.save(html_file_path)

    def run(self):
        self.read_csv()
        self.process_data()
        self.create_map()

if __name__ == '__main__':
    # Usage example 1:
    geo_graph = GeoSpatialGraph('MyUSAVisit.csv')
    geo_graph.run()
    geo_graph.save_map_html('MyUSAVisit.html')

    # Usage example 2:
    geo_graph = GeoSpatialGraph('FullMyUSAVisit.csv')
    geo_graph.run()
    geo_graph.save_map_html('FullMyUSAVisit.html')