from data import *
from scipy import stats
from utils import *


class Analysis(object):

    def __init__(self):
        self.subject_list = pd.read_csv(DISTRICT_CSV)[SUBJECT].unique()
        self.district_list = pd.read_csv(DISTRICT_CSV)[DISTRICT].unique()
        self.subject_district_list = pd.read_csv(DISTRICT_CSV)

    # Описательная статистика
    def descriptive_st(self, file_name, factor):
        assert factor in [YEAR, SUBJECT, DISTRICT, None], 'Некорректный фактор анализа'

        df = pd.read_csv(file_name)
        indicator = gen_label(file_name)

        factor_list = []
        if factor is not None:
            if factor == YEAR:
                factor_list = pd.read_csv(YEARS_CSV)[YEAR].values
            elif factor == SUBJECT:
                factor_list = self.subject_list
            else:
                factor_list = self.district_list

        fin_df = pd.DataFrame({INDICATOR: [], 'factor': [], 'factor value': [], 'count': [], 'mean': [],
                           'std': [], 'min': [], 'max': [], 'normality': []})

        for f in factor_list:
            sorted_df = df[df[factor] == f][INDICATOR]

            ds = sorted_df.describe()

            alpha = 0.05
            stat, p = stats.normaltest(sorted_df)
            pirson = False
            if p > alpha:
                pirson = True

            fin_df.loc[len(fin_df)] = [indicator, factor, f, ds.loc['count'], ds.loc['mean'],
                                   ds.loc['std'], ds.loc['min'], ds.loc['max'], pirson]

        if os.path.exists(DESCRIPTIVE_NAME):
            read_df = pd.read_csv(DESCRIPTIVE_NAME)
            read_df = read_df.append(fin_df, ignore_index=True)
            read_df.drop_duplicates()
            read_df.to_csv(DESCRIPTIVE_NAME, index=False)
        else:
            fin_df.to_csv(DESCRIPTIVE_NAME, index=False)

        # paintHist(file_name, indicator, factor)


    # Анализ динамических рядов
    def analysis_time_series(self, file_name):
        df = pd.read_csv(file_name)

        districts = self.subject_district_list
        fin_df = pd.DataFrame()
        fin_general_df = pd.DataFrame()

        for _,row in districts.iterrows():
            subject = row[SUBJECT]
            district = row[DISTRICT]
            data = df[(df[SUBJECT] == subject) & (df[DISTRICT] == district)]

            years_list = data[YEAR].tolist()
            int_y = [int(x) for x in years_list]
            indicators = data[INDICATOR].tolist()
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

            data.insert(data.shape[1], 'абсолют. прирост базисных', abs_inc_basic)
            data.insert(data.shape[1], 'абсолют. прирост цепных', abs_inc_chain)
            data.insert(data.shape[1], 'темп роста базисных, %', growth_rate_of_basic)
            data.insert(data.shape[1], 'темп роста цепных, %', growth_rate_of_chain)
            data.insert(data.shape[1], 'темп прироста базисных, %', growth_inc_of_basic)
            data.insert(data.shape[1], 'темп прироста цепных, %', growth_inc_of_chain)

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
            fin_df = fin_df.append(data, ignore_index=True)
            fin_general_df = fin_general_df.append(general_df, ignore_index=True)

        fin_df.to_csv(TIME_SERIES_NAME + gen_label(file_name) + CSV, index=False)
        fin_general_df.to_csv(TIME_SERIES_NAME + 'gen_' + gen_label(file_name) + CSV, index=False)

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

        if os.path.exists(GROUP_COMPARISON_NAME):
            read_df = pd.read_csv(GROUP_COMPARISON_NAME)
            read_df = read_df.append(df, ignore_index=True)
            read_df.drop_duplicates()
            read_df.to_csv(GROUP_COMPARISON_NAME, index=False)
        else:
            df.to_csv(GROUP_COMPARISON_NAME, index=False)

        # paintBox(data, data2, name, name2)

    def corr_regression(self, file1, file2):
        data_x = pd.read_csv(file1)
        data_y = pd.read_csv(file2)

        name_x = gen_label(file1)
        name_y = gen_label(file2)

        data = Data().combine_indicators(data_x, data_y, name_x, name_y)
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
            print('Связь слабая')
        elif abs(r) > 0.6:
            print('Связь тесная')
        else:
            print('Связь умеренная')

        print(f'Regression line: y={intercept:.2f}+{slope:.2f}x\n'
            f'Regression coefficient: r={r:.2f}')

        # paintCorrelation(fx, fy, slope, intercept, r, name_x, name_y)