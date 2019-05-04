import pandas as pd
import json
from geojson import Feature, FeatureCollection, Point

input_file = 'data/WigleWifi.csv'

#loads file, selects header from
#second row down as per mobile export.
data = pd.read_csv(input_file, encoding = "ISO-8859-1", low_memory=False, nrows=200000, header =1)

#drops all rows with a ? in location data
data=data[data.CurrentLatitude != "?"]

#Print tail to confirm load
print(data.tail())


#filters to cleanse data
data=data[data.AccuracyMeters < 20]
data=data[data.MAC == '']

#ar_filtered = data[data.AccuracyMeters < 20]
#ar_filtered2 = (ar_filtered[ar_filtered.MAC == 'c0:3f:0e:7c:d5:b5'])



print(data[['MAC','SSID','CurrentLatitude','CurrentLongitude']])


#export a geoJSON object


features = data.apply(
    lambda row: Feature(geometry=Point((float(row['CurrentLongitude']), float(row['CurrentLatitude'])))),
    axis=1).tolist()

# all the other columns used as properties
#properties = ar_filtered.drop((['MAC','SSID']), axis=1).to_dict('records')

# whole geojson object
feature_collection = FeatureCollection(features=features)#, properties=properties)



with open('file.geojson', 'w', encoding='utf-8') as f:
    json.dump(feature_collection, f, ensure_ascii=False)
jsonFile = data.to_json(orient='records')


