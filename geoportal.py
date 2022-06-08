import json
import pandas as pd
import main
from utils import YEAR, SUBJECT, DISTRICT, DISTRICT_CSV, \
    INDICATOR, YEAR_GEO, SUBJECT_GEO, DISTRICT_GEO, INDICATOR_GEO


def gen_geo_inc(file_name, out_file_name):
    regs = pd.read_csv(DISTRICT_CSV)[[SUBJECT, DISTRICT]].values
    df = pd.DataFrame({YEAR: [], SUBJECT: [], DISTRICT: [], 'абсолют. прирост цепных': [],
                       'темп прироста цепных, %': []})

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


def add_data(file_geo, file_df, indicator, column_names, column_geo_names, out_file):
    columns = column_names.split('&')
    columns_geo = column_geo_names.split('&')

    geojson = pd.read_json(file_geo)
    data = {'type': 'FeatureCollection', 'features': []}
    df = pd.read_csv(file_df)
    list_ = []

    for feature in geojson['features']:
        property = feature['properties']
        geometry = feature['geometry']

        value = property[SUBJECT] + property[DISTRICT]
        if value in list_:
            continue
        list_.append(value)

        df_new_property = df[(df[SUBJECT].str.contains(property[SUBJECT])) &
                             (df[DISTRICT].str.contains(property[DISTRICT]))]
        df_new_property.at[:, SUBJECT] = property[SUBJECT]
        df_new_property.at[:, DISTRICT] = property[DISTRICT]
        df_new_property.at[:, INDICATOR] = indicator

        df_new_property.rename(columns={INDICATOR: INDICATOR_GEO, YEAR: YEAR_GEO,
                                        SUBJECT: SUBJECT_GEO, DISTRICT: DISTRICT_GEO}, inplace=True)
        for idx, c in enumerate(columns):
            df_new_property.rename(columns={c: columns_geo[idx]}, inplace=True)

        cols = [INDICATOR_GEO, YEAR_GEO, SUBJECT_GEO, DISTRICT_GEO] + columns_geo
        df_new_property = df_new_property[cols]

        for _,row in df_new_property.iterrows():
            f = {'type': 'Feature',
                 'geometry': geometry,
                 'properties': {}}
            for c in cols:
                if c == YEAR_GEO:
                    f['properties'][c] = int(row[c])
                else:
                    f['properties'][c] = row[c]
            data['features'].append(f)

    with open(out_file, 'w') as f:
        json.dump(data, f)


def read_geojson(file):
    geojson = pd.read_json(file)
    print(geojson['type'])
    for feature in geojson['features']:
        print(feature['properties'])