import json
from utils import *


def generate_geojson_from_df_time_series(file_geo, file_df, indicator, ind, column_names, out_file):
    columns = column_names.split('&')
    for geo in file_geo:
        geojson = pd.read_json(geo)
        data = {'type': 'FeatureCollection', 'features': []}
        df = pd.read_csv(file_df)
        df = df[df[INDICATOR_GEO] == indicator]
        list_ = []
        subject = ''

        for feature in geojson['features']:
            property = feature['properties']
            geometry = feature['geometry']

            subject = property[SUBJECT]
            value = property[SUBJECT] + property[DISTRICT]
            if value in list_:
                continue
            list_.append(value)

            df_new_property = df[(df[SUBJECT].str.contains(property[SUBJECT])) &
                             (df[DISTRICT].str.contains(property[DISTRICT]))]
            print(df_new_property)
            df_new_property.at[:, SUBJECT] = property[SUBJECT]
            df_new_property.at[:, DISTRICT] = property[DISTRICT]
            df_new_property.at[:, INDICATOR_GEO] = ind

            df_new_property.rename(columns={YEAR: YEAR_GEO, SUBJECT: SUBJECT_GEO,
                                        DISTRICT: DISTRICT_GEO}, inplace=True)

            cols = [INDICATOR_GEO, YEAR_GEO, SUBJECT_GEO, DISTRICT_GEO] + columns
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

        with open(out_file + subject + '.geojson', 'w') as f:
            json.dump(data, f)


def read_geojson_content(file):
    geojson = pd.read_json(file)
    print(geojson['type'])
    for feature in geojson['features']:
        print(feature['properties'])