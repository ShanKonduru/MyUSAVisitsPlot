import geopandas as gpd
import folium
from folium import plugins
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class GeoSpatialGraph:
    def __init__(self, csv_file, launch_graph=True):
        self.csv_file = csv_file
        self.launch_graph = launch_graph
        self.df = None
        self.us_states = None
        self.merged_data = None
        self.map = None
        self.html_outputs = []  # List to store HTML outputs
        
    def generate_datetime_stamp(self):
        # Generates a datetime stamp in ISO 8601 format.
        # Returns: str: Datetime stamp string in the format 'YYYY-MM-DDTHH-MM-SS'.
        now = datetime.now()
        datetime_stamp = now.strftime("_%Y%m%d%H%M%S_")
        return datetime_stamp

    def generate_html_page(self, title, description, image_src, image_alt, template_path, output_file):
        # Read the HTML template from the specified file
        with open(template_path, "r") as template_file:
            html_template = template_file.read()

        # Format the HTML template with the provided values
        final_html = html_template.format(title=title, description=description, image_src=image_src, image_alt=image_alt)

        # Write the HTML content to the specified file
        with open(output_file, "w") as html_file:
            html_file.write(final_html)

        print(f"HTML page generated successfully. Saved to {output_file}")
 
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

    def generate_visits_graph(self):
        title = 'Number of Visits by State Over the Years'
        # Extract the year from the visited_date column
        self.df['Year'] = pd.to_datetime(self.df['visited_date']).dt.year

        # Group by state and year, count the number of visits
        grouped_data = self.df.groupby(['state_abbr', 'Year']).size().reset_index(name='Visits')

        # Pivot the data for easy plotting
        pivot_data = grouped_data.pivot(index='Year', columns='state_abbr', values='Visits').fillna(0)

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = pivot_data.plot(kind='bar', stacked=False, ax=ax)
        
        plt.xlabel('Year')
        plt.ylabel('# of Visits')
        plt.title(title)
        plt.legend(title='State', bbox_to_anchor=(1, 1))

        # Add data labels to each bar
        for bar in bars.patches:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='top')
            
        timestamp = self.generate_datetime_stamp()
        image_file = "SampleImages/" + title.replace(' ', '_') +  timestamp + ".png"
        plt.savefig(image_file)

        if(self.launch_graph):
            plt.show()
            plt.close()
        
        html_file_name = "html_files/" + title.replace(' ', '_') + ".html"

        self.generate_html_page(
            title=title,
            description='Number of Visits by State Over the Years',
            image_src=image_file,
            image_alt=image_file,
            template_path="templates/image_html_template.html",
            output_file=html_file_name
        )
        
    def generate_state_wise_visits_graph(self):
        title = 'Total Number of Days Stayed in Each State'
        # Group by state, calculate the total number of days stayed
        total_days_per_state = self.df.groupby('State_Name')['Days_stayed'].sum()

        # Plotting
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = total_days_per_state.sort_values().plot(kind='bar', ax=ax, color='blue', alpha=0.7)
        plt.xlabel('State Name')
        plt.ylabel('Total Days Stayed')
        plt.title(title)

        # Add data labels to each bar
        for bar in bars.patches:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

        plt.xticks(rotation=45, ha='right')  # Rotate state names for better readability
        plt.tight_layout()

        timestamp = self.generate_datetime_stamp()
        image_file = "SampleImages/" + title.replace(' ', '_') +  timestamp + ".png"
        plt.savefig(image_file)

        if(self.launch_graph):
            plt.show()
            plt.close()

        html_file_name = "html_files/" + title.replace(' ', '_') + ".html"

        self.generate_html_page(
            title=title,
            description='Total Number of Days Stayed in Each State',
            image_src=image_file,
            image_alt=image_file,
            template_path="templates/image_html_template.html",
            output_file=html_file_name
        )


    def generate_average_visits_graph(self):
        title = 'Average Number of Days Stayed Over the Years'

        # Extract the year from the visited_date column
        self.df['Year'] = pd.to_datetime(self.df['visited_date']).dt.year

        # Group by year, calculate the average number of days stayed
        avg_days_per_year = self.df.groupby('Year')['Days_stayed'].mean()

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = avg_days_per_year.plot(kind='bar', ax=ax, color='blue', alpha=0.7)
        plt.xlabel('Year')
        plt.ylabel('Average Days Stayed')
        plt.title(title)
        
        # Add data labels to each bar
        for bar in bars.patches:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='top')

        timestamp = self.generate_datetime_stamp()
        image_file = "SampleImages/" + title.replace(' ', '_') +  timestamp + ".png"
        plt.savefig(image_file)

        if(self.launch_graph):
            plt.show()
            plt.close()

        html_file_name = "html_files/" + title.replace(' ', '_') + ".html"

        self.generate_html_page(
            title=title,
            description='Average Number of Days Stayed Over the Years',
            image_src=image_file,
            image_alt=image_file,
            template_path="templates/image_html_template.html",
            output_file=html_file_name
        )


    def generate_geo_spatial_graph(self, html_file_path):
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

        # Save the map as an HTML file
        self.map.save(html_file_path)
        
    def run_generate_geo_spatial_graph(self):
        self.read_csv()
        self.process_data()
        self.generate_geo_spatial_graph(html_file_path="html_files\generate_geo_spatial_graph.html")

    def run_generate_other_graph(self):
        self.read_csv()
        self.process_data()
        self.generate_visits_graph()
        self.generate_average_visits_graph()
        self.generate_state_wise_visits_graph()

if __name__ == '__main__':
    # Usage example 1:
    geo_graph = GeoSpatialGraph('MyUSAVisit.csv', launch_graph=True)
    geo_graph.run_generate_geo_spatial_graph()
    geo_graph.run_generate_other_graph()
    # Usage example 2:
    geo_graph = GeoSpatialGraph('FullMyUSAVisit.csv', launch_graph=True)
    geo_graph.run_generate_geo_spatial_graph()
    geo_graph.run_generate_other_graph()
