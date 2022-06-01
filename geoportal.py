import pandas as pd
import main
from utils import YEAR, SUBJECT, DISTRICT, DISTRICT_CSV

def gen_geo_inc(file_name, out_file_name):
    regs = pd.read_csv(DISTRICT_CSV)[[SUBJECT, DISTRICT]].values
    df = pd.DataFrame({YEAR: [], SUBJECT: [], DISTRICT: [], 'абсолют. прирост цепных': [], 'темп прироста цепных, %': []})

    for reg in regs:
        subject = reg[0]
        district = reg[1]

        f = main.analysis_time_series(file_name, subject, district, True)
        f = f[[YEAR, SUBJECT, DISTRICT, 'абсолют. прирост цепных', 'темп прироста цепных, %']]
        df = pd.concat([df, f], ignore_index=True)
        df = df.reset_index(drop=True)

    df.to_csv(out_file_name, index=False)


def df_to_geojson(file):
    df = pd.read_csv(file)
    geojson = {'type': 'FeatureCollection', 'features': []}
    properties = df.columns.tolist()
    for _,row in df.iterrows():
        feature = {'type': 'Feature',
                   'properties': {},
                   'geometry': {'type': 'Point',
                                'coordinates': []}}
        for p in properties:
            feature['properties'][p] = row[p]
        geojson['features'].append(feature)
    for feature in geojson['features']:
        print(feature['properties'])

def read_j():
    geojson = pd.read_json('geojson_data/здоровьеКрасноярск.geojson')
    for feature in geojson['features']:
        print(feature['geometry'])