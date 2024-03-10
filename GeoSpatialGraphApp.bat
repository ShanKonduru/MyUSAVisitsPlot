@echo off

poetry run python GeoSpatialGraphApp.py

REM http://localhost:5050/GeoSpatialGraph?InputData=MyUSAVisit.csv
REM http://localhost:5050/GeoSpatialGraph?InputData=FullMyUSAVisit.csv

REM start "MyUSAVisit" "http://localhost:5050/GeoSpatialGraph?InputData=MyUSAVisit.csv"

REM start "FullMyUSAVisit" "http://localhost:5050/GeoSpatialGraph?InputData=FullMyUSAVisit.csv"