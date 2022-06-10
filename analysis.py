import matplotlib.pyplot as plt
from scipy import stats
from utils import *
import seaborn as sns


class Analysis(object):

    def __init__(self):
        district_csv = pd.read_csv(DISTRICT_CSV)
        self.years = pd.read_csv(YEARS_CSV)[YEAR].values
        self.regs = district_csv[[SUBJECT, DISTRICT]].values
        self.subject_district_df = district_csv

    # Описательная статистика
    def descriptive_st(self, file_name, property, factor):
        assert factor in [YEAR, SUBJECT, DISTRICT], 'Некорректный фактор анализа'

        df = pd.read_csv(file_name)

        if factor == YEAR:
            factor_list = self.years
        elif factor == SUBJECT:
            factor_list = self.subject_district_df[SUBJECT].unique()
        else:
            factor_list = self.subject_district_df[DISTRICT].unique()

        fin_df = pd.DataFrame({INDICATOR: [], 'factor': [], 'factor value': [], 'count': [],
                               'mean': [], 'std': [], 'min': [], 'max': [], 'normality': []})

        for f in factor_list:
            sorted_df = df[df[factor] == f][property]
            print(sorted_df)
            sorted_df = sorted_df.dropna()
            print(sorted_df)

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

        append_row_to_file(DESCRIPTIVE_NAME, fin_df)

        # paintHist(file_name, indicator, factor)

    # Анализ динамических рядов
    def analysis_time_series(self, file_name, property):
        df = pd.read_csv(file_name)
        out_name = property.replace(':', ',')

        districts = self.subject_district_df
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

            prop_list = ['абсолют. прирост базисных', 'абсолют. прирост цепных',
                         'темп роста базисных, %', 'темп роста цепных, %',
                         'темп прироста базисных, %', 'темп прироста цепных, %']

            data.insert(data.shape[1], prop_list[0], abs_inc_basic)
            data.insert(data.shape[1], prop_list[1], abs_inc_chain)
            data.insert(data.shape[1], prop_list[2], growth_rate_of_basic)
            data.insert(data.shape[1], prop_list[3], growth_rate_of_chain)
            data.insert(data.shape[1], prop_list[4], growth_inc_of_basic)
            data.insert(data.shape[1], prop_list[5], growth_inc_of_chain)

            with_year = str(years_list[0])
            on_year = str(years_list[len(years_list) - 1])

            general_df = pd.DataFrame({SUBJECT: [], DISTRICT: [], 'период': [], 'средний уровень ряда': [],
                                       'средний абс. прирост': [], 'средний темп роста, %': [],
                                       'средний темп прироста, %': [], })

            if data.shape[0] != 1:
                av_row = (0.5 * (f_ind[0] + f_ind[len(f_ind) - 1]) + sum(f_ind[1:len(f_ind) - 1])) / (data.shape[0] - 1)
                av_abs_inc = (f_ind[len(f_ind) - 1] - f_ind[0]) / (data.shape[0] - 1)
                av_growth_rate = pow(f_ind[len(f_ind) - 1] / f_ind[0], 1 / (data.shape[0] - 1)) * 100
                av_inc_rate = av_growth_rate - 100

                general_df.loc[len(general_df)] = [subject, district, with_year + '-' + on_year,
                                                   round(av_row, 2), round(av_abs_inc, 2),
                                                   round(av_growth_rate, 2), round(av_inc_rate, 2)]

            # paintDynamicDiagram(int_y, f_ind, district, years_list)
            fin_df = fin_df.append(data[[YEAR, SUBJECT, DISTRICT] + prop_list], ignore_index=True)
            fin_general_df = fin_general_df.append(general_df, ignore_index=True)

        print(fin_df)
        fin_df.to_csv(TIME_SERIES_NAME + out_name + CSV, index=False)
        fin_general_df.to_csv(TIME_SERIES_NAME + 'gen_' + out_name + CSV, index=False)

    def group_comparison(self, file, file2, dependency):
        data = pd.read_csv(file)
        data2 = pd.read_csv(file2)

        name = gen_label(file)
        name2 = gen_label(file2)

        x = data[INDICATOR]
        y = data2[INDICATOR]

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

        df.loc[len(df)] = [name, name2, mean_1, mean_2, std_1, std_2, difference]

        append_row_to_file(GROUP_COMPARISON_NAME, df)

        # paintBox(data, data2, name, name2)

    def corr_regression(self, file1, file2):
        data_x = pd.read_csv(file1)
        data_y = pd.read_csv(file2)

        name_x = gen_label(file1)
        name_y = gen_label(file2)

        data = combine_indicators(data_x, data_y, name_x, name_y,
                                  self.years, self.regs)
        data = data.drop(data[data.isnull().T.any()].index)

        x = data[name_x].values
        y = data[name_y].values

        fx = [float(n) for n in x]
        fy = [float(n) for n in y]

        slope, intercept, r, p, stderr = stats.linregress(fx, fy)
        print(slope)
        print(intercept)
        print(r)
        print(p)
        print(stderr)

        if abs(r) < 0.3:
            print(CORRELATION[0])
        elif abs(r) > 0.6:
            print(CORRELATION[2])
        else:
            print(CORRELATION[3])

        print(f'Regression line: y={intercept:.2f}+{slope:.2f}x\n'
              f'Regression coefficient: r={r:.2f}')

        # paintCorrelation(fx, fy, slope, intercept, r, name_x, name_y)


# объединение 2 показателей в один csv
def combine_indicators(data_x, data_y, name_x, name_y, years, regs):
    data = pd.DataFrame({YEAR: [], SUBJECT: [], DISTRICT: [], name_x: [], name_y: []})

    for year in years:
        for reg in regs:
            subject = reg[0]
            district = reg[1]
            value1 = data_x[(data_x[YEAR] == year) & (data_x[SUBJECT] == subject)
                            & (data_x[DISTRICT] == district)][INDICATOR].tolist()
            value2 = data_y[(data_y[YEAR] == year) & (data_y[SUBJECT] == subject)
                            & (data_y[DISTRICT] == district)][INDICATOR].tolist()
            if (bool(value1) & bool(value2)):
                data.loc[len(data)] = [year, subject, district,
                                       float(data_x[(data_x[YEAR] == year) & (data_x[SUBJECT] == subject)
                                                    & (data_x[DISTRICT] == district)][INDICATOR]),
                                       float(data_y[(data_y[YEAR] == year) & (data_y[SUBJECT] == subject)
                                                    & (data_y[DISTRICT] == district)][INDICATOR])]
    return data


@staticmethod
def t(df, df2):
    f = pd.read_csv(df)
    f2 = pd.read_csv(df2)
    f['смертность'] = f2['смертность на 100 тыс. нас.']
    h = f.corr()
    print(f.corr())
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.subplots_adjust(0.25, 0.25, 0.93, 0.93)
    sns.heatmap(h, ax=ax, cmap="YlGnBu", linewidths=0.1, annot=True)
    plt.show()