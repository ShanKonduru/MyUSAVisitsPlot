@echo off
poetry run python GeoSpatialGraph.py

start "MyUSAVisit" "MyUSAVisit.html"

start "FullMyUSAVisit" "FullMyUSAVisit.html"


poetry run python GeoSpatialGraphApp.py

start "MyUSAVisit" "http://localhost:5050/GeoSpatialGraph?InputData=MyUSAVisit.csv"

start "FullMyUSAVisit" "http://localhost:5050/GeoSpatialGraph?InputData=FullMyUSAVisit.csv"