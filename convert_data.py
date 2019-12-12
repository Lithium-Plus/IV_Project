import csv
import os
import pandas as pd
import json
from time import strptime
import shapely
from shapely.geometry import shape, Point,Polygon
with open(r'info_viz\InformationVisualization\IV_Project\zillow-neighborhoods.geojson') as f:
    data = json.load(f)


df = pd.read_csv(r'info_viz\InformationVisualization\IV_Project\Annual_Crime_Dataset_2015withLongLad.csv')
df['neighborhood'] = ''


for feature in data['features']:
    name = feature['properties']['name']
    # print(feature['geometry']['coordinates'])
    print(name)
    if len(feature['geometry']['coordinates'][0])>3:
        polygon = Polygon(feature['geometry']['coordinates'][0])
        count = 0
        area = polygon.area
        monthly = [0 for i in range(12)]
        for index, row in df.iterrows():
            # print(type(row))
            # print(row)
            point = Point((float(row['Longitude']),float(row['Latitude'])))
            if polygon.contains(point):
                count += 1
                date = row['GO Report Date']
                month = date.split('-')[1]
                month_num = strptime(month,'%b').tm_mon
                monthly[month_num-1] += 1
                row['neighborhood'] = name
        feature['properties']['density'] = count/(1000*area)
        feature['properties']['monthly'] = monthly

df.to_csv(r'info_viz\InformationVisualization\IV_Project\crime_data_with_neiborhood.csv')
with open(r'info_viz\InformationVisualization\IV_Project\neiborhood_data.geojson','w') as f:
    json.dump(data, f)


