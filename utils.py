import pandas as pd
import os

YEAR = 'год'
YEAR_GEO = 'year'
SUBJECT_WITH_DISTRICT = 'субъект,район'
SUBJECT = 'субъект'
SUBJECT_GEO = 'subject'
DISTRICT = 'район'
DISTRICT_GEO = 'district'
INDICATOR = 'показатель'
INDICATOR_GEO = 'indicator'
SPACE = ' '
YEARS_CSV = 'csv_data/годы.csv'
DISTRICT_CSV = 'csv_data/районы.csv'
CSV = '.csv'
EXCEL = '.xlsx'
NONE_STR = 'None'
DATA_DIR = 'csv_data/'
ANALYSIS_DIR = 'csv_data/analysis/'
RES = 'results.csv'
DESCRIPTIVE_DIR = 'csv_data/analysis/descriptive_stat/'
TIME_SERIES_DIR = 'csv_data/analysis/time_series/'
GROUP_COMPARISON_DIR = 'csv_data/analysis/group_comparison/'
CORR_REGR_DIR = 'csv_data/analysis/corr_regr/'
CORRELATION = ['слабая', 'сильная', 'умеренная']

CSV_PROP = 'csv_data/new_properties.csv'
CSV_PROP_IND = ['смертность на 100 тыс. нас.',                  # 0
                'рождаемость на 100 тыс. нас.',                 # 1
                'естеств. прирост на 100 тыс. нас.',            # 2
                'количество врачей на 100 тыс. нас.',           # 3
                'заболеваемость 0-14 лет на 100 тыс. нас.',     # 4
                'заболеваемость 15-17 лет на 100 тыс. нас.',    # 5
                'младенческая смертность на 1000 нас.']         # 6
CSV_11 = 'csv_data/11_абсолютное значение.csv'
CSV_11_IND = [  'общая численность населения: всего',                   # 0
    'численность сельского населения',                                  # 1
    'численность детей (0-14 лет включительно)',                        # 2
    'численность детей (0-1 год в возрасте «0» лет)',                   # 3
    'численность подростков (от 15 до 17 лет включительно)',            # 4
    'численность взрослого населения территории (от 18 лет и старше)',  # 5
    'численность работающего населения: всего',                         # 6
    'численность работающих женщин',                                    # 7
    'общее число родившихся детей',                                     # 8
    'количество детей, родившихся живыми',                              # 9
    'количество умерших в данном календарном году, всего:',             # 10
    'количество умерших детей в возрасте до 1 года',                    # 11
    'число умерших от злокачественных новообразований: всего',          # 12
    'число умерших от злокачественных новообразований желудка',         # 13
    'число умерших от новообразований кожи (кроме меланомы)',           # 14
    'число умерших от злокачественных новообразований щитовидной железы',       # 15
    'число умерших от злокачественных новообразований трахеи, бронхов, легкого',# 16
    'число умерших от лейкемии',                                        # 17
    'общее число родившихся детей живыми и мертвыми']                   # 18
CSV_31 = 'csv_data/31_значение.csv'
CSV_31_IND = ['расходы на здравоохранение',                                  # 0
    'расходы на образование',                                                # 1
    'среднедушевой доход населения',                                         # 2
    'прожиточный минимум',                                                   # 3
    'стоимость минимальной продуктовой корзины',                             # 4
    'процент лиц с доходами ниже прожиточного минимума',                     # 5
    'количество жилой площади на 1 человека',                                # 6
    'процент квартир, не имеющих водопровода',                               # 7
    'процент квартир, не имеющих канализации',                               # 8
    'удельный вес жилой площади, оборудованной центральным отоплением',      # 9
    'площадь жилищ, приходящихся в среднем на одного жителя на конец года',  # 10
    'фактическое конечное потребление домашних хозяйств на душу населения',  # 11
    'валовой региональный продукт (валовая добавленная стоимость) на душу населения',# 12
    'среднемесячная номинальная начисленная заработная плата работающих в экономике',# 13
    'стоимость основных фондов отраслей экономики на душу населения',        # 14
    'инвестиции в основной капитал на душу населения',                       # 15
    'количество врачей всех специальностей',                                 # 16
    'количество среднего медперсонала',                                      # 17
    'число посещений поликлинических медицинских учреждений на одного врача',# 18
    'число посещений поликлинических медицинских учреждений',                # 19
    'количество врачей поликлинических медицинских учреждений',              # 20
    'число лиц, которым оказана медицинская помощь при выездах',             # 21
    'численность лиц, поступивших в больничные учреждения',                  # 22
    'отношение среднедушевого дохода к величине прожиточного минимума']     # 23
CSV_23_0_14 = 'csv_data/23_от 0-14 лет абс..csv'
CSV_23_15_17 = 'csv_data/23_15-17 лет абс..csv'
CSV_23_18_ = 'csv_data/23_от 18 абс..csv'
CSV_23_IND = ['заболеваемость всего:',                                      # 0
    'анемии' 'сахарный диабет i типа',                                      # 1
    'сахарный диабет ii типа',                                              # 2
    'ожирение',                                                             # 3
    'болезни, характеризующиеся повышенным кровяным давлением',             # 4
    'бронхит хронический и неуточнённый,\nэмфизема',                        # 5
    'астма, астматический статус',                                          # 6
    'язва желудка и 12-ти перстной кишки',                                  # 7
    'гастрит и дуоденит',                                                   # 8
    'мочекаменная болезнь',                                                 # 9
    'врожденные аномалии (пороки развития), деформации и хромосомные нарушения у детей'] # 10
CSV_27_0_14 = 'csv_data/27_0-14 лет абс..csv'
CSV_27_15_17 = 'csv_data/27_15-17 лет абс..csv'
CSV_27_18_60 = 'csv_data/27_18-60 абс..csv'
CSV_27_IND = ['психические расстройства, всего'                                 # 0
    'невротические, связанные со стрессом и соматоформные расстройства'         # 1
    'другие непсихотические расстройства'                                       # 2
    'синдром зависимости от алкоголя (алкоголизм)'                              # 3
    'синдром зависимости от наркотических веществ (наркомания)'                 # 4
    'поведенческие синдромы, непсихотические расстройства детского и подросткового возраста'] # 5
CSV_28_B = 'csv_data/28_мужчины знач.csv'
CSV_28_G = 'csv_data/28_женщины знач..csv'
CSV_28_IND = ['число дней временной нетрудоспособности'
    'число случаев временной нетрудоспособности']


# изъятие основной части файла -
# удаление префикса и постфикса (расширения)
def gen_name(name):
    return name.split('/').pop().removesuffix(CSV)


# добавление информации в файл построчно
def append_row_to_file(file_name, df):
    if os.path.exists(file_name):
        read_df = pd.read_csv(file_name)
        read_df = read_df.append(df, ignore_index=True)
        read_df = read_df.drop_duplicates()
        read_df.to_csv(file_name, index=False)
    else:
        df.to_csv(file_name, index=False)


# добавление информации в файл по столбцам
def append_col_to_file(file_name, df, col_name):
    if os.path.exists(file_name):
        read_df = pd.read_csv(file_name)
        read_df[col_name] = df[col_name]
        read_df.to_csv(file_name, index=False)
    else:
        df.to_csv(file_name, index=False)

# создание всех директорий
def add_all_dir():
    dir_list = [DATA_DIR, ANALYSIS_DIR, DESCRIPTIVE_DIR,
                TIME_SERIES_DIR, CORR_REGR_DIR, GROUP_COMPARISON_DIR]
    for dir in dir_list:
        if not os.path.exists(dir):
            os.mkdir(dir.removesuffix('/'))