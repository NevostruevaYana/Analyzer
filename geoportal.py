import json
import pandas as pd
import main
from utils import YEAR, SUBJECT, DISTRICT, DISTRICT_CSV, \
    INDICATORS, INDICATOR

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


def add_data(file_geo, file_df, indicator, column_names, out_file):
    # Сброс ограничений на число столбцов
    pd.set_option('display.max_columns', None)
    # Сброс ограничений на количество символов в записи
    pd.set_option('display.max_colwidth', None)

    columns = column_names.split('&')

    geojson = pd.read_json(file_geo)
    with open(file_geo, encoding='utf-8') as f:
        data = json.load(f)
    df = pd.read_csv(file_df)
    list_ = []

    for feature in geojson['features']:
        property = feature['properties']
        geometry = feature['geometry']

        value = property[SUBJECT] + property[DISTRICT]
        if value in list_:
            continue
        list_.append(value)

        new_property = df[(df[SUBJECT].str.contains(property[SUBJECT])) &
                          (df[DISTRICT].str.contains(property[DISTRICT]))]
        new_property.loc[:, SUBJECT] = property[SUBJECT]
        new_property.loc[:, DISTRICT] = property[DISTRICT]
        new_property.loc[:, INDICATORS] = indicator
        cols = [YEAR, SUBJECT, DISTRICT, INDICATORS] + columns
        new_property = new_property[cols]

        for _,row in new_property.iterrows():
            f = {'type': 'Feature',
                 'geometry': geometry,
                 'properties': {}}
            for c in cols:
                if c == YEAR:
                    f['properties'][c] = int(row[c])
                else:
                    f['properties'][c] = row[c]
            data['features'].append(f)

    with open(out_file, 'w') as f:
        json.dump(data, f)


def read_j(file):
    # geojson = pd.read_json('geojson_data/здоровьеКрасноярск.geojson')
    geojson = pd.read_json(file)
    for feature in geojson['features']:
        print(feature['properties'])