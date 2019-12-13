import csv
import os
import pandas as pd
import json
from time import strptime
from datetime import datetime
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
        solved = 0
        area = polygon.area
        monthly = [0 for i in range(12)]
        robbery = 0
        burglary = 0
        auto_theft = 0
        agg_assault = 0
        rape = 0
        theft = 0
        days = []
        for index, row in df.iterrows():
            point = Point((float(row['Longitude']),float(row['Latitude'])))
            if polygon.contains(point):
                count += 1
                date = row['GO Report Date']
                month = date.split('-')[1]
                month_num = strptime(month,'%b').tm_mon
                monthly[month_num-1] += 1
                row['neighborhood'] = name
                if row['Clearance Status'] == 'C':
                    solved += 1
                    report_date = row['GO Report Date'][:-2] + '20' + row['GO Report Date'][-2:]
                    clear_date = row['Clearance Date'][:-2] + '20' + row['Clearance Date'][-2:]
                    delta = datetime.strptime(clear_date, '%d-%b-%Y').date() - datetime.strptime(report_date, '%d-%b-%Y').date()
                    days.append(delta.days)
                if row['Highest NIBRS/UCR Offense Description'] == 'Robbery':
                    robbery+=1
                elif row['Highest NIBRS/UCR Offense Description'] == 'Burglary':
                    burglary +=1 
                elif row['Highest NIBRS/UCR Offense Description'] == 'Auto Theft':
                    auto_theft +=1
                elif row['Highest NIBRS/UCR Offense Description'] == 'Agg Assault':
                    agg_assault += 1
                elif row['Highest NIBRS/UCR Offense Description'] == 'Theft':
                    theft +=1
                elif row['Highest NIBRS/UCR Offense Description'] == 'Rape':
                    rape += 1
                    print('rape')

        feature['properties']['density'] = count/(1000*area)
        feature['properties']['monthly'] = monthly
        feature['properties']['clearance_rate'] = solved/count if count > 0 else 0
        feature['properties']['robbery'] = robbery
        feature['properties']['burglary'] = burglary
        feature['properties']['auto_theft'] = auto_theft
        feature['properties']['agg_assault'] = agg_assault
        feature['properties']['theft'] = theft
        feature['properties']['rape'] = rape
        
        if len(days) > 0:
            feature['properties']['avg_days_solve'] = sum(days)/len(days)
        else:
            feature['properties']['avg_days_solve'] = 0

df.to_csv(r'info_viz\InformationVisualization\IV_Project\crime_data_with_neiborhood.csv')
with open(r'info_viz\InformationVisualization\IV_Project\neiborhood_data.geojson','w') as f:
    json.dump(data, f)


