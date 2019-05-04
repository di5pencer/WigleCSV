import pandas as pd
import json
from geojson import Feature, FeatureCollection, Point

input_file = 'data/WigleWifi.csv'

# loads file, selects header from
# second row down as per mobile export.
# limited to 200,000 rows
data = pd.read_csv(input_file, encoding="ISO-8859-1", low_memory=False, nrows=200000, header=1)

# Print tail to confirm load
print(data.tail())

# filters to cleanse data
# drops all rows with a ? in location data
data = data[data.CurrentLatitude != "?"]

# removes all rows with poor accuracy
data = data[data.AccuracyMeters < 20]

# uncomment to filter by MAC
# data=data[data.MAC == ' Enter Mac to Filter in here']

# prints results
print(data[['MAC', 'SSID', 'CurrentLatitude', 'CurrentLongitude']])

# export a geoJSON object
features = data.apply(
    lambda row: Feature(geometry=Point((float(row['CurrentLongitude']), float(row['CurrentLatitude'])))),
    axis=1).tolist()

# all the other columns used as properties
# properties = ar_filtered.drop((['MAC','SSID']), axis=1).to_dict('records')
# whole geojson object
feature_collection = FeatureCollection(features=features)  # , properties=properties)

with open('file.geojson', 'w', encoding='utf-8') as f:
    json.dump(feature_collection, f, ensure_ascii=False)
jsonFile = data.to_json(orient='records')
