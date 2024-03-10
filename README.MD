# My USA Visit Dashboard

## Overview

This project generates dashboards based on my USA Visit data using Python. It utilizes various libraries, such as Geopandas, Folium, Pandas, HoloViews, NumPy, and Matplotlib, to create interactive and informative visualizations.

## Installation

To set up the project, ensure you have Python 3.11 installed. Use [Poetry](https://python-poetry.org/) to manage dependencies. Run the following commands in your terminal:

```bash
poetry install
```

This will install the required packages specified in `pyproject.toml`.

## Usage

### Data Sources

Make sure you have the necessary data sources before running the program. The project uses the `ne_110m_admin_1_states_provinces` shapefile to map the United States.
this can be downloaded from https://indexhu.carto.com/tables/ne_110m_admin_1_states_provinces_lines/public

### Running the Program

```bash
poetry run python  plotMe.py
```

This command will execute the program and generate an HTML dashboard named `visited_places_map.html`. Open this file in a web browser to view the interactive map.

## Dependencies

- Python 3.11
- Geopandas 0.14.3
- Folium 0.16.0
- Pandas 2.2.1
- HoloViews 0.9.2
- NumPy 1.26.4
- Matplotlib 3.8.3

## Development

If you want to contribute or modify the code, create a virtual environment and install the development dependencies using:

```bash
poetry install --dev
```

## Sample HTML

## Sample HTML Page

Here is the content of a sample HTML page:

[Link to Sample HTML Page](https://github.com/ShanKonduru/MyUSAVisitsPlot/html_files/generate_geo_spatial_graph.html)


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, feel free to contact:

```bash
- Author: ShanKonduru
- Email: ShanKonduru@gmail.com
- Git Repository: https://github.com/ShanKonduru/MyUSAVisitsPlot
```
