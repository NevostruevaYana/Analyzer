import matplotlib.pyplot as plt
import seaborn as sns
from utils import *


class Graphics(object):

    def plot_descr_stat(self, df):
        ind_list = df[INDICATOR_GEO].unique()
        for g in [YEAR, SUBJECT]:
            fig, ax = plt.subplots()
            for i in ind_list:
                f = df[(df['indicator'] == i) & (df['factor'] == g)]['factor value']
                ff = df[(df['indicator'] == i) & (df['factor'] == g)]['mean']
                if not (f.empty | ff.empty):
                    ax.plot(f, ff, marker='o', label=i)
                    plt.title(f'Среднее значения для показателя\n"{i}"')
                    plt.xlabel(g)
                    plt.xticks(f, rotation=30, fontsize=8, ha='right')
                    plt.legend(fontsize=8)
                    plt.tight_layout()
                    plt.grid()
                    plt.savefig(f'{DESCRIPTIVE_DIR}{g}_{i}')
                    plt.cla()
            plt.close(fig)


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
                    plt.title('Сравнение показателей \'mean\'')
                    plt.xlabel(g)
                    if g == YEAR:
                        ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, -0.25),
                            fancybox=True, shadow=True, ncol=2)
                    else:
                        ax.legend(fontsize=6, bbox_to_anchor=(1, 0.5))
                    plt.xticks(x, rotation=30, fontsize=8, ha='right')
                    plt.tight_layout()
                    plt.grid()
                    plt.savefig(f'{DESCRIPTIVE_DIR}{g}_{out_name}.png')
                    plt.cla()
            plt.close(fig)

    def plot_time_series(self, df):
        subjects = df[SUBJECT].unique()
        indicator = df[INDICATOR_GEO].unique()
        indicator = indicator[0].replace(':', ',')
        for subject in subjects:
            fig, ax = plt.subplots()
            df_ = df[df[SUBJECT] == subject]
            districts = df_[DISTRICT].unique()
            for district in districts:
                df__ = df_[df_[DISTRICT] == district]
                x = df__[YEAR]
                y = df__['abs inc basic']
                if not (x.empty | y.empty):
                    ax.plot(x, y, marker='o', label=district)
                    plt.xticks(x)
                    ax.set_title(f'Абсолютный прирост базисных показателя\n\'{indicator}\''
                         f'\n{subject}')
                    plt.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, -0.3),
                        fancybox=True, shadow=True, ncol=2)
                    ax.set_xlabel('Год')
                    plt.tight_layout()
                    plt.grid()
                    plt.savefig(f'{TIME_SERIES_DIR}{indicator}_{subject}.png')
            plt.close(fig)

    def plot_box(self, data, data2, name, name2, factor, f):
        fig, ax = plt.subplots()
        plt.boxplot([data, data2],
                    labels=[name, name2])
        plt.xticks(rotation=20, fontsize=8, ha='right')
        ax.set_title(f'Сравнение групп\n{factor} {f}')
        ax.set_xlabel('показатели')
        plt.tight_layout()
        plt.grid()
        fig_name_1 = name.split(' на')[0]
        fig_name_2 = name2.split(' на')[0]
        plt.savefig(f'{GROUP_COMPARISON_DIR}{f}_{fig_name_1}_{fig_name_2}.png')
        plt.close(fig)

    def plot_multi_box(self, ind_list, data_list, out_name):
        fig, ax = plt.subplots()
        plt.boxplot(data_list,
                    labels=ind_list)
        plt.xticks(rotation=20, fontsize=8, ha='right')
        ax.set_title(f'Сравнение групп для \n\'{out_name}\'')
        ax.set_xlabel('показатели')
        plt.tight_layout()
        plt.grid()
        plt.savefig(f'{GROUP_COMPARISON_DIR}{out_name}')
        plt.close(fig)


    def plot_corr_matrix(self, corr_matrix, png_name):
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(corr_matrix, ax=ax, cmap="Blues", linewidths=0.1, annot=True, square=True)
        plt.yticks(fontsize=10)
        plt.xticks(rotation=20, fontsize=10, ha='right')
        plt.tight_layout()
        plt.savefig(f'{CORR_REGR_DIR}{png_name}')
        plt.close(fig)

    def plot_corr_gegr(self, x, y, x_name, y_name, slope, intercept, cor, r2):
        x_name = x_name.replace(':', ' ')
        y_name = y_name.replace(':', ' ')
        line = slope * x + intercept
        fig, ax = plt.subplots()
        plt.scatter(x, y, s=50)
        plt.plot(x, line, 'r', label=f'y={round_to_1(slope)}x+{round_to_1(intercept)}')
        plt.plot([], [], ' ', label=f'R = {cor}')
        plt.plot([], [], ' ', label=f'R_sq = {r2}')
        ax.grid(True)
        ax.legend(fontsize=12)
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.yticks(fontsize=8)
        plt.xticks(rotation=8)
        plt.tight_layout()
        plt.savefig(f'{CORR_REGR_DIR}{x_name}_{y_name}.png')
        plt.close(fig)