## Introduction

Exploring data provided by openstreetmap. You can export Stockholm data from https://www.openstreetmap.org/export#map=13/59.3244/18.0835 .
Use the file read_osm.py to generate the sqlite database. Currently only the tags "amenity", "railway" and "leasure" are taken into consideration.

Once the sqlite database has been generated, the interactive heatmaps maps can be generated with show_map.py

## Dependencies
imposm, sqlite3, folium
