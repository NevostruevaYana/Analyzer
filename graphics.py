import matplotlib.pyplot as plt
import seaborn as sns
from utils import *


class Graphics(object):

    def __init__(self):
        self.colors = ['g', 'b', 'y', 'r', 'k', 'm', 'c']

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

    def plot_descr_stat(self, df):
        print(df)
        ind_list = df[INDICATOR_GEO].unique()
        for g in [YEAR, SUBJECT]:
            for i in ind_list:
                fig, ax = plt.subplots()
                f = df[(df['indicator'] == i) & (df['factor'] == g)]['factor value']
                ff = df[(df['indicator'] == i) & (df['factor'] == g)]['mean']
                if not (f.empty | ff.empty):
                    ax.plot(f, ff, marker='o', label=i)
                    plt.title(f'Среднее значения для показателя\n"{i}"')
                    plt.xlabel(g)
                    plt.legend(fontsize=8)
                    plt.xticks(rotation=30, fontsize=8, ha='right')
                    plt.tight_layout()
                    plt.grid()
                    plt.savefig(f'{DESCRIPTIVE_DIR}{g}_{i}')


    # отображение нескольких показателей описательной статистики на 1 графике
    def plot_multi_descr_stat(self, ind_list, out_name):
        df = pd.read_csv('csv_data/analysis/descriptive_stat/results.csv')
        for g in [YEAR, SUBJECT]:
            fig, ax = plt.subplots()
            for i in ind_list:
                x = df[(df['indicator'] == i) & (df['factor'] == g)]['factor value']
                y = df[(df['indicator'] == i) & (df['factor'] == g)]['mean']
                if not (x.empty | y.empty):
                    ax.plot(x, y, marker='o', label=i)
            plt.title('Сравнение показателей')
            plt.xlabel(g)
            if g == YEAR:
                ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, -0.25),
                    fancybox=True, shadow=True, ncol=2)
            else:
                ax.legend(fontsize=6, bbox_to_anchor=(1, 0.5))
            plt.xticks(rotation=30, fontsize=8, ha='right')
            plt.tight_layout()
            plt.grid()
            plt.savefig(f'{DESCRIPTIVE_DIR}{g}_{out_name}.png')

    def plot_time_series(self, df):
        subjects = df[SUBJECT].unique()
        for subject in subjects:
            df_ = df[df[SUBJECT] == subject]
            districts = df_[DISTRICT].unique()
            fig, ax = plt.subplots()
            for district in districts:
                df__ = df_[df_[DISTRICT] == district]
                x = df__[YEAR]
                y = df__['abs inc basic']
                if not (x.empty | y.empty):
                    ax.plot(x, y, marker='o', label=district)
            ax.grid(True)
            ax.set_title('Абсолютный прирост базисных показателя\n')
            plt.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, -0.3),
          fancybox=True, shadow=True, ncol=2)
            ax.set_xlabel('Год')
            ax.set_ylabel('Показатель')
            plt.tight_layout()
            plt.savefig(f'{TIME_SERIES_DIR}{subject}.png')

    def plot_box(self, data, data2, name, name2):
        fig, ax = plt.subplots()
        plt.boxplot([data, data2],
                    labels=[name, name2])
        plt.xticks(rotation=20, fontsize=8, ha='right')
        ax.set_title('Сравнение групп')
        ax.set_xlabel('показатели')
        ax.set_ylabel('значения')
        plt.tight_layout()
        plt.grid()
        fig_name_1 = name.split(' на')[0]
        fig_name_2 = name2.split(' на')[0]
        plt.savefig(f'{GROUP_COMPARISON_DIR}{fig_name_1}_{fig_name_2}.png')

    def plot_multi_box(self, ind_list, out_name):
        df = pd.read_csv(CSV_PROP)
        data_list = []
        for indicator in ind_list:
            data_list.append(df[indicator].dropna())
            print(data_list)
        plt.boxplot(data_list,
                    labels=ind_list)
        plt.xticks(rotation=20, fontsize=8, ha='right')
        plt.tight_layout()
        plt.grid()
        plt.savefig(f'{GROUP_COMPARISON_DIR}{out_name}.png')


    def plot_corr_matrix(self, corr_matrix):
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(corr_matrix, ax=ax, cmap="Blues", linewidths=0.1, annot=True, square=True)
        plt.yticks(fontsize=8)
        plt.xticks(rotation=20, fontsize=8, ha='right')
        plt.tight_layout()
        plt.savefig(f'{CORR_REGR_DIR}')

    def plot_corr_gegr(self, x, y, x_name, y_name, slope, intercept, cor, r2):
        line = slope * x + intercept
        fig, ax = plt.subplots()
        plt.scatter(x, y, s=50)
        plt.plot(x, line, 'r', label='y={:.2f}x+{:.2f}'.format(slope, intercept))
        plt.plot([], [], ' ', label=f'R = {cor}')
        plt.plot([], [], ' ', label=f'R_sq = {r2}')
        ax.grid(True)
        ax.legend(fontsize=12)
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.yticks(fontsize=8)
        plt.xticks(rotation=8)
        plt.tight_layout()
        plt.savefig(f'{CORR_REGR_DIR}{x_name}_{y_name}')