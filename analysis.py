import pandas as pd

from graphics import Graphics
from scipy import stats
from utils import *
from sklearn.metrics import r2_score


class Analysis(object):

    def __init__(self):
        district_csv = pd.read_csv(DISTRICT_CSV)
        self.years_df = pd.read_csv(YEARS_CSV)
        self.subjects_districts_df = district_csv
        self.g = Graphics()

    # Описательная статистика
    def descriptive_stat(self, file_name, properties, factor):
        assert factor in [YEAR, SUBJECT, DISTRICT], 'Некорректный фактор анализа'

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

    def group_comparison(self, file_name_1, property_1, file_name_2, property_2, dependency):

        data = pd.read_csv(file_name_1)
        x = data[property_1]

        if file_name_1 == file_name_2:
            y = data[property_2]
        else:
            data_2 = pd.read_csv(file_name_2)
            y = data_2[property_2]

        x = x.dropna()
        y = y.dropna()

        df = pd.DataFrame({'group 1': [], 'group 2': [], 'mean 1': [], 'mean 2': [],
                           'std 1': [], 'std 2': [], 'the presence of differences': []})

        stat_x, px = stats.normaltest(x)  # Критерий согласия Пирсона
        stat_y, py = stats.normaltest(y)
        pirson_x = False
        pirson_y = False
        alpha = 0.05
        if px > alpha:
            pirson_x = True
        if py > alpha:
            pirson_y = True

        mean_1 = round(x.mean(), 2)
        mean_2 = round(y.mean(), 2)
        std_1 = round(x.std(), 2)
        std_2 = round(y.std(), 2)

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
            property_1 = f'{gen_name(file_name_1)}_{property_1}'
            property_2 = f'{gen_name(file_name_2)}_{property_2}'

        df.loc[len(df)] = [property_1, property_2, mean_1, mean_2, std_1, std_2, difference]

        append_row_to_file(f'{GROUP_COMPARISON_DIR}{RES}', df)

        self.g.plot_box(x, y, property_1, property_2)

    # корреляционная регрессия (возможна как линейная, так и множественная)
    def multiple_corr_regr(self, files_list, properties_list_x, properties_list_y):
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
                r2 = r2_score(d[x], d[y])
                cor = r

                if abs(cor) < 0.3:
                    c = CORRELATION[0]
                elif abs(cor) > 0.6:
                    c = CORRELATION[1]
                else:
                    c = CORRELATION[2]
                print(c)

                fin_df.loc[len(fin_df)] = [x, y, round(cor, 2), round(stderr, 2), round(r**2, 2)]

                self.g.plot_corr_gegr(d[x], d[y], x, y, slope, intercept, cor, r2)

        append_row_to_file(f'{CORR_REGR_DIR}{RES}', fin_df)
