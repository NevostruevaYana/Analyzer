import json
from utils import *


def generate_geojson_from_df(file_geo, file_df, indicator, column_names,
                             column_geo_names, out_file):
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


def read_geojson_content(file):
    geojson = pd.read_json(file)
    print(geojson['type'])
    for feature in geojson['features']:
        print(feature['properties'])