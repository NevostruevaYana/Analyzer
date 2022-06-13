import matplotlib.pyplot as plt
import pandas as pd
from utils import *

from utils import gen_name


class Graphics(object):

    def __init__(self):
        self.colors = ['g', 'b', 'y', 'r', 'k', 'm', 'c']

    def paintPointDiagram(self, df, col_name, y_label):
        x = list(range(1, len(df) + 1))
        y = df[col_name].tolist()

        fig, ax = plt.subplots()
        ax.scatter(x, y, c='r', s=1)
        ax.set_xlabel('номер региона')
        ax.set_ylabel(gen_name(y_label))
        ax.grid()
        plt.show()

    def paintHist(self, file_name, indicator, year):
        fig, ax = plt.subplots()
        ax.set_title(gen_name(file_name))
        ax.hist(indicator)
        if year is None:
            ax.set_xlabel('показатель за весь период')
        else:
            ax.set_xlabel('показатель в ' + str(year) + ' году')
        ax.set_ylabel('количество районов, входящих в интервал')
        plt.show()

    def paintDynamicDiagram(self, int_y, f_ind, district, years_list):
        fig, ax = plt.subplots()
        ax.plot(int_y, f_ind, 'o-')
        ax.grid(True)
        ax.set_title('Ряд динамики\n' + district + ' с ' + str(years_list[0]) + ' по ' + str(
            years_list[len(years_list) - 1]) + ' гг.')
        ax.set_xlabel('Год')
        ax.set_ylabel('Показатель')
        plt.show()

    def paintBox(self, data, data2, name, name2):
        plt.boxplot([data['показатель'], data2['показатель']],
                    labels=[gen_name(name), gen_name(name2)])
        plt.show()

    def paintCorrelation(self, x, y, slope, intercept, r, name_x, name_y):
        fig, ax = plt.subplots()

        ax.scatter(x, y, c='k', s=2, label='Data points')
        ffy = [x * slope + intercept for x in x]
        line = f'Regression line: y={intercept:.2f}+{slope:.2f}x\nr={r:.2f}'
        ax.plot(x, ffy, label=line)

        ax.set_xlabel(name_x)
        ax.set_ylabel(name_y)
        ax.legend(facecolor='white')
        plt.show()

    def plot_descr_stat(self):
        df = pd.read_csv('csv_data/analysis/descriptive_st.csv')
        indicators = df['indicator'].drop_duplicates().values
        for indicator in indicators:
            df_ = df[df['indicator'] == indicator]
            for factor in [YEAR, SUBJECT]:
                df__ = df_[df['factor'] == factor]
                if not df__.empty:
                    for property in ['mean', 'min', 'max']:
                        fig, ax = plt.subplots()
                        ax.plot(df__['factor value'], df__[property], marker='o')
                        plt.title(indicator)
                        plt.xlabel(factor)
                        plt.ylabel(property)
                        plt.xticks(rotation=30, fontsize=8, ha='right')
                        plt.tight_layout()
                        plt.grid()
                        plt.savefig(f'{DESCRIPTIVE_DIR}{property}_{factor}_{indicator}.png')