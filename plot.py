import matplotlib.pyplot as plt
from utils import gen_label


class Plot:

    @staticmethod
    def paintPointDiagram(df, col_name, y_label):
        x = list(range(1, len(df) + 1))
        y = df[col_name].tolist()

        fig, ax = plt.subplots()
        ax.scatter(x, y, c='r', s=1)
        ax.set_xlabel('номер региона')
        ax.set_ylabel(gen_label(y_label))
        ax.grid()
        plt.show()

    @staticmethod
    def paintHist(file_name, indicator, year):
        fig, ax = plt.subplots()
        ax.set_title(gen_label(file_name))
        ax.hist(indicator)
        if year is None:
            ax.set_xlabel('показатель за весь период')
        else:
            ax.set_xlabel('показатель в ' + str(year) + ' году')
        ax.set_ylabel('количество районов, входящих в интервал')
        plt.show()

    @staticmethod
    def paintDynamicDiagram(int_y, f_ind, district, years_list):
        fig, ax = plt.subplots()
        ax.plot(int_y, f_ind, 'o-')
        ax.grid(True)
        ax.set_title('Ряд динамики\n' + district + ' с ' + str(years_list[0]) + ' по ' + str(
            years_list[len(years_list) - 1]) + ' гг.')
        ax.set_xlabel('Год')
        ax.set_ylabel('Показатель')
        plt.show()

    @staticmethod
    def paintBox(data, data2, name, name2):
        plt.boxplot([data['показатель'], data2['показатель']],
                    labels=[gen_label(name), gen_label(name2)])
        plt.show()

    @staticmethod
    def paintCorrelation(x, y, slope, intercept, r, name_x, name_y):
        fig, ax = plt.subplots()

        ax.scatter(x, y, c='k', s=2, label='Data points')
        ffy = [x * slope + intercept for x in x]
        line = f'Regression line: y={intercept:.2f}+{slope:.2f}x\nr={r:.2f}'
        ax.plot(x, ffy, label=line)

        ax.set_xlabel(name_x)
        ax.set_ylabel(name_y)
        ax.legend(facecolor='white')
        plt.show()