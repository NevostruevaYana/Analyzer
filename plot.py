import pandas as pd
import matplotlib.pyplot as plt


class Plot:

    @staticmethod
    def checkBD(csv, y):
        f = pd.read_csv(csv)
        f_num = list(range(1, len(f) + 1))
        f_zn = f[y].tolist()

        fig, ax = plt.subplots()
        ax.set_title(str(csv).replace('.csv', ''))
        ax.scatter(f_num, f_zn, c='r', s=1)
        ax.set_xlabel('Номер региона')
        ax.set_ylabel('Показатель смертности на 100 тыс. нас.')
        ax.grid()
        plt.show()