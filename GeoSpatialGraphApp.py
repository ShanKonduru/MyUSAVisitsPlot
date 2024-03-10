from flask import Flask, render_template, request
import os
from GeoSpatialGraph import GeoSpatialGraph  

app = Flask(__name__)

@app.route('/GeoSpatialGraph')
def geo_spatial_graph():
    input_data = request.args.get('InputData')

    if input_data:
        csv_file_path = os.path.join(os.getcwd(), input_data)

        if os.path.exists(csv_file_path):
            geo_graph = GeoSpatialGraph(csv_file_path)
            geo_graph.run()

            html_content = geo_graph.map._repr_html_()
            return html_content
        else:
            return f"Error: CSV file '{input_data}' not found."

    return "Error: InputData parameter is missing."

if __name__ == '__main__':
    app.run(host='localhost', port=5050, debug=True)
