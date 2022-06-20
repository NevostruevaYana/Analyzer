import numpy
import pandas as pd

from graphics import Graphics
from scipy import stats
from utils import *
from sklearn.metrics import r2_score


class Analysis(object):

    def __init__(self):
        assert os.path.exists(YEARS_CSV), 'Файл с годами не существует'
        assert os.path.exists(DISTRICT_CSV), 'Файл с районами не существует'
        district_csv = pd.read_csv(DISTRICT_CSV)
        self.years_df = pd.read_csv(YEARS_CSV)
        self.subjects_districts_df = district_csv
        self.g = Graphics()

    # Описательная статистика
    def descriptive_stat(self, file_name, properties, factor):
        assert factor in [YEAR, SUBJECT], 'Некорректный фактор анализа'

        df = pd.read_csv(file_name)

        if factor == YEAR:
            factor_list = self.years_df[YEAR].values
        else:
            factor_list = self.subjects_districts_df[SUBJECT].unique()

        fin_df = pd.DataFrame({INDICATOR_GEO: [], 'factor': [], 'factor value': [], 'count': [],
                               'mean': [], 'std': [], 'min': [], 'max': [], 'normality': []})

        for property in properties:

            for f in factor_list:
                sorted_df = df[df[factor] == f][property]
                sorted_df = sorted_df.dropna()

                ds = sorted_df.describe()

                alpha = 0.05
                stat, p = stats.normaltest(sorted_df)
                print(p)
                pirson = False
                if p > alpha:
                    pirson = True

                fin_df.loc[len(fin_df)] = [property, factor, f, round(ds.loc['count'], 2),
                                           round(ds.loc['mean'], 2), round(ds.loc['std'], 2),
                                           round(ds.loc['min'], 2), round(ds.loc['max'], 2), round(pirson, 2)]

        append_row_to_file(f'{DESCRIPTIVE_DIR}{RES}', fin_df)
        self.g.plot_descr_stat(fin_df)

    # Анализ динамических рядов
    def time_series(self, file_name, property):
        df = pd.read_csv(file_name)

        districts = self.subjects_districts_df
        fin_df = pd.DataFrame()
        fin_general_df = pd.DataFrame()

        for _, row in districts.iterrows():
            subject = row[SUBJECT]
            district = row[DISTRICT]
            data = df[(df[SUBJECT] == subject) & (df[DISTRICT] == district)]

            years_list = data[YEAR].tolist()
            int_y = [int(x) for x in years_list]
            indicators = data[property].tolist()
            f_ind = [float(x) for x in indicators]

            abs_inc_basic = list()
            abs_inc_chain = list()
            growth_rate_of_basic = list()
            growth_rate_of_chain = list()
            growth_inc_of_basic = list()
            growth_inc_of_chain = list()
            first_ind = f_ind[0]

            for i in f_ind:
                i = round(i, 2)
                abs_inc_basic.append(round(i - f_ind[0], 2))
                abs_inc_chain.append(round(i - first_ind, 2))
                gg = i / f_ind[0] * 100
                growth_rate_of_basic.append(round(gg, 2))
                jj = i / first_ind * 100
                growth_rate_of_chain.append(round(jj, 2))
                growth_inc_of_basic.append(round(gg - 100, 2))
                growth_inc_of_chain.append(round(jj - 100, 2))
                first_ind = i

            prop_list = ['abs inc basic', 'abs inc chain',
                         'growth rate of basic, %', 'growth rate of chain, %',
                         'growth inc of basic, %', 'growth inc of chain, %']

            data.insert(data.shape[1], prop_list[0], abs_inc_basic)
            data.insert(data.shape[1], prop_list[1], abs_inc_chain)
            data.insert(data.shape[1], prop_list[2], growth_rate_of_basic)
            data.insert(data.shape[1], prop_list[3], growth_rate_of_chain)
            data.insert(data.shape[1], prop_list[4], growth_inc_of_basic)
            data.insert(data.shape[1], prop_list[5], growth_inc_of_chain)

            with_year = str(years_list[0])
            on_year = str(years_list[len(years_list) - 1])

            general_df = pd.DataFrame({INDICATOR_GEO: [], SUBJECT_GEO: [], DISTRICT_GEO: [], 'period': [], 'av_row': [],
                                       'av abs inc': [], 'av growth rate, %': [], 'av inc rate, %': []})

            if data.shape[0] != 1:
                av_row = (0.5 * (f_ind[0] + f_ind[len(f_ind) - 1]) + sum(f_ind[1:len(f_ind) - 1])) / (data.shape[0] - 1)
                av_abs_inc = (f_ind[len(f_ind) - 1] - f_ind[0]) / (data.shape[0] - 1)
                av_growth_rate = pow(f_ind[len(f_ind) - 1] / f_ind[0], 1 / (data.shape[0] - 1)) * 100
                av_inc_rate = av_growth_rate - 100

                general_df.loc[len(general_df)] = [property, subject, district, with_year + '-' + on_year,
                                                   round(av_row, 2), round(av_abs_inc, 2),
                                                   round(av_growth_rate, 2), round(av_inc_rate, 2)]

            data[INDICATOR_GEO] = property
            fin_df = fin_df.append(data[[INDICATOR_GEO, YEAR, SUBJECT, DISTRICT] + prop_list], ignore_index=True)
            fin_general_df = fin_general_df.append(general_df, ignore_index=True)

        append_row_to_file(TIME_SERIES_DIR + RES, fin_df)
        self.g.plot_time_series(fin_df)
        append_row_to_file(f'{TIME_SERIES_DIR}gen_{RES}', fin_general_df)

    # сравнение групп
    def group_comparison(self, factor, file_name_1, property_1, file_name_2, property_2, dependency=False):
        assert factor in [YEAR, SUBJECT], 'Некорректный фактор анализа'

        if factor == YEAR:
            factor_list = self.years_df[YEAR].values
        else:
            factor_list = self.subjects_districts_df[SUBJECT].unique()

        df_ = pd.read_csv(file_name_1)

        for f in factor_list:
            data = df_
            data = data[data[factor] == f]
            x = data[property_1]

            if file_name_1 == file_name_2:
                y = data[property_2]
            else:
                data_2 = pd.read_csv(file_name_2)
                y = data_2[property_2]

            x = x.dropna()
            y = y.dropna()

            if (len(x) < 20) & (len(y) < 20):
                continue

            df = pd.DataFrame({'factor': [], 'factor value':[], 'the presence of differences': [],
                                'group 1': [], 'mean 1': [], 'std 1': [],
                                'group 2': [], 'mean 2': [], 'std 2': []})

            pirson_x = check_pirson_criteria(x)
            pirson_y = check_pirson_criteria(x)

            mean_x, std_x = get_mean_std(x)
            mean_y, std_y = get_mean_std(y)

            if (pirson_x & pirson_y):
                if (dependency):
                    # 2 зависимые выборки (normal)
                    t = stats.ttest_rel(x, y)
                else:
                    # 2 независимые выборки (normal)
                    t = stats.ttest_ind(x, y)
            else:
                if (dependency):
                    # 2 зависимые группы
                    t = stats.wilcoxon(x, y)
                else:
                    # 2 независимые группы
                    t = stats.mannwhitneyu(x, y)

            difference = True
            if t[1] > 0.05:
                difference = False

            if property_1 == property_2:
                property_1_ = f'{gen_name(file_name_1)}_{property_1}'
                property_2_ = f'{gen_name(file_name_2)}_{property_2}'
            else:
                property_1_ = property_1
                property_2_ = property_2

            df.loc[len(df)] = [factor, f, difference, property_1_, mean_x, std_x, property_2_, mean_y, std_y]
            append_row_to_file(f'{GROUP_COMPARISON_DIR}{RES}', df)
            self.g.plot_box(x, y, property_1_, property_2_, factor, f)

    # сравнение 3 и более групп
    def multi_group_comparison(self, factor, files_list, properties_list, out_png_name, dependency=False):
        assert factor in [YEAR, SUBJECT], 'Некорректный фактор анализа'
        global mean_4, std_4, mean_5, std_5, df_4, df_5

        args_len = len(properties_list)
        assert (args_len < 6) & (args_len > 2), 'Можно сравнивать от 3 до 5 групп'

        if factor == YEAR:
            factor_list = self.years_df[YEAR].values
        else:
            factor_list = self.subjects_districts_df[SUBJECT].unique()

        data = pd.read_csv(files_list[0])

        if len(files_list) > 1:
            for i in range(1, len(files_list)):
                data_ = pd.read_csv(files_list[i])
                data = pd.concat([data, data_], axis=1)

        df_ = data[[factor] + properties_list]

        for f in factor_list:
            data = df_
            data = data[data[factor] == f]

            df_1 = data[properties_list[0]].dropna()
            df_2 = data[properties_list[1]].dropna()
            df_3 = data[properties_list[2]].dropna()

            if (len(df_1) < 20) & (len(df_2) < 20) & (len(df_3) < 20):
                continue

            pirson_1 = check_pirson_criteria(df_1)
            pirson_2 = check_pirson_criteria(df_2)
            pirson_3 = check_pirson_criteria(df_3)
            pirson_fin = pirson_1 & pirson_2 & pirson_3

            mean_1, std_1 = get_mean_std(df_1)
            mean_2, std_2 = get_mean_std(df_2)
            mean_3, std_3 = get_mean_std(df_3)

            if args_len == 3:
                if (pirson_fin):
                    # 3 независимые выборки (normal)
                    t = stats.f_oneway(df_1, df_2, df_3)
                else:
                    if (dependency):
                        # 3 зависимые группы
                        t = stats.friedmanchisquare(df_1, df_2, df_3)
                    else:
                        # 3 независимые группы
                        t = stats.kruskal(df_1, df_2, df_3)
            else:
                df_4 = data[properties_list[3]].dropna()
                if len(df_4) < 20:
                    continue
                mean_4, std_4 = get_mean_std(df_4)
                pirson_4 = check_pirson_criteria(df_4)
                pirson_fin = pirson_fin & pirson_4

                if args_len == 4:
                    if (pirson_fin):
                        # 4 независимые выборки (normal)
                        t = stats.f_oneway(df_1, df_2, df_3, df_4)
                    else:
                        if (dependency):
                            # 4 зависимые группы
                            t = stats.friedmanchisquare(df_1, df_2, df_3, df_4)
                        else:
                            # 4 независимые группы
                            t = stats.kruskal(df_1, df_2, df_3, df_4)
                else:
                    df_5 = data[properties_list[4]].dropna()
                    if len(df_5) < 20:
                        continue
                    mean_5, std_5 = get_mean_std(df_5)
                    pirson_5 = check_pirson_criteria(df_5)
                    pirson_fin = pirson_fin & pirson_5

                    if (pirson_fin):
                        # 3 и более независимые выборки (normal)
                        t = stats.f_oneway(df_1, df_2, df_3, df_4, df_5)
                    else:
                        if (dependency):
                            # 3 и более зависимые группы
                            t = stats.friedmanchisquare(df_1, df_2, df_3, df_4, df_5)
                        else:
                            # 3 и более независимые группы
                            t = stats.kruskal(df_1, df_2, df_3, df_4, df_5)

            difference = True
            if t[1] > 0.05:
                difference = False

            df_list = [df_1, df_2, df_3]

            if args_len == 3:
                df = pd.DataFrame({'factor': [], 'factor value': [], 'the presence of differences': [],
                                    'group 1': [], 'mean 1': [], 'std 1': [],
                                    'group 2': [], 'mean 2': [], 'std 2': [], 'group 3': [], 'mean 3': [], 'std 3': []})
                df.loc[len(df)] = [factor, f, difference, properties_list[0], mean_1, std_1,
                           properties_list[1], mean_2, std_2, properties_list[2], mean_3, std_3]
            elif args_len == 4:
                df = pd.DataFrame({'factor': [], 'factor value': [], 'the presence of differences': [], 'group 1': [], 'mean 1': [], 'std 1': [],
                               'group 2': [], 'mean 2': [], 'std 2': [], 'group 3': [], 'mean 3': [], 'std 3': [],
                               'group 4': [], 'mean 4': [], 'std 4': []})
                df.loc[len(df)] = [factor, f, difference, properties_list[0], mean_1, std_1,
                               properties_list[1], mean_2, std_2, properties_list[2], mean_3, std_3,
                               properties_list[3], mean_4, std_4]
                df_list = df_list + [df_4]
            else:
                df = pd.DataFrame({'factor': [], 'factor value': [], 'the presence of differences': [], 'group 1': [], 'mean 1': [], 'std 1': [],
                               'group 2': [], 'mean 2': [], 'std 2': [], 'group 3': [], 'mean 3': [], 'std 3': [],
                               'group 4': [], 'mean 4': [], 'std 4': [], 'group 5': [], 'mean 5': [], 'std 5': []})
                df.loc[len(df)] = [factor, f, difference, properties_list[0], mean_1, std_1,
                               properties_list[1], mean_2, std_2, properties_list[2], mean_3, std_3,
                               properties_list[3], mean_4, std_4, properties_list[4], mean_5, std_5]
                df_list = df_list + [df_4, df_5]

            append_row_to_file(f'{GROUP_COMPARISON_DIR}{RES}', df)
            self.g.plot_multi_box(properties_list[0:args_len], df_list[0:args_len], f'{f}_{out_png_name}')

    # корреляционная регрессия (возможна как линейная, так и множественная)
    def correlation_regression(self, files_list, properties_list_x, properties_list_y):
        properties_list = properties_list_x + properties_list_y

        data = pd.read_csv(files_list[0])

        if len(files_list) > 1:
            for i in range(1, len(files_list)):
                data_ = pd.read_csv(files_list[i])
                data = pd.concat([data, data_], axis=1)

        if properties_list:
            data = data[properties_list]
        else:
            data = data.drop(columns=[YEAR, SUBJECT, DISTRICT])

        data = data.dropna(how='all')

        corr_matrix = data.corr()

        try:
            png_name = len(pd.read_csv(CORR_REGR_DIR + RES))
        except FileNotFoundError:
            png_name = '1'

        self.g.plot_corr_matrix(corr_matrix, png_name)

        fin_df = pd.DataFrame({'property_1': [], 'property_2': [], 'corr_coeff': [],
                               'stderr': [], 'R^2': []})

        for x in properties_list_x:
            for y in properties_list_y:
                print(x + '  ' + y)
                d = data[[x, y]]
                d = d.dropna(how='any')

                slope, intercept, r, p, stderr = stats.linregress(d[x], d[y])
                print(p)
                cor = r

                if abs(cor) < 0.3:
                    c = CORRELATION[0]
                elif abs(cor) > 0.6:
                    c = CORRELATION[1]
                else:
                    c = CORRELATION[2]
                print(c)

                fin_df.loc[len(fin_df)] = [x, y, round(cor, 2), round(stderr, 2), round(r**2, 2)]

                self.g.plot_corr_gegr(d[x], d[y], x, y, slope, intercept, round(cor, 2), round(r**2, 2))

        append_row_to_file(f'{CORR_REGR_DIR}{RES}', fin_df)


def check_pirson_criteria(df):
    stat, p = stats.normaltest(df)  # Критерий согласия Пирсона
    pirson = False
    alpha = 0.05
    if p > alpha:
        pirson = True
    return pirson


def get_mean_std(df):
    mean = round(df.mean(), 2)
    std = round(df.std(), 2)
    return (mean, std)