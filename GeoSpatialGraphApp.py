from flask import Flask, render_template, request, send_from_directory
import os
from GeoSpatialGraph import GeoSpatialGraph

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Data Visualization App!"

@app.route('/GeoSpatialGraph')
def geo_spatial_graph():
    input_data = request.args.get('InputData')

    if input_data:
        csv_file_path = os.path.join(os.getcwd(), input_data)

        if os.path.exists(csv_file_path):
            geo_graph = GeoSpatialGraph(csv_file_path, launch_graph=False)
            geo_graph.run_generate_geo_spatial_graph()

            # Generate HTML content for Geo Spatial Graph
            geo_spatial_html = geo_graph.map._repr_html_()  # Assuming Geo Spatial Graph uses Folium map

            # Render the template with Geo Spatial Graph
            return render_template('geo_spatial_graph_template.html', geo_spatial_graph=geo_spatial_html)
        else:
            return f"Error: CSV file '{input_data}' not found."

    return "Error: InputData parameter is missing."

@app.route('/OtherGraphs')
def other_graphs():
    input_data = request.args.get('InputData')

    if input_data:
        csv_file_path = os.path.join(os.getcwd(), input_data)

        if os.path.exists(csv_file_path):
            geo_graph = GeoSpatialGraph(csv_file_path, launch_graph=False)
            geo_graph.run_generate_other_graph()

            # Generate HTML content for other graphs (excluding Geo Spatial Graph)
            other_graphs_html = '\n'.join(geo_graph.html_outputs[-3:])  # Exclude the first element which is for Geo Spatial Graph
            print(geo_graph.html_outputs[-3:])

            # Render the template with other graphs
            return render_template('other_graphs_template.html', other_graphs=other_graphs_html)
        else:
            return f"Error: CSV file '{input_data}' not found."

    return "Error: InputData parameter is missing."

# Serve HTML files directly without using send_file
@app.route('/html_files/<path:filename>')
def html_files(filename):
    return send_from_directory(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'html_files'), filename)

if __name__ == '__main__':
    app.run(host='localhost', port=5050, debug=True)
