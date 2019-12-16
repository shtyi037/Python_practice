import os
import sys
import datetime as dt
import numpy as np


G_WeekDays = ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')

def dmy2Weekday(dmy):
    return dt.datetime.strptime(str(dmy, encoding='utf-8'),
                                '%d-%m-%Y').date().weekday()


def ReadData(filename):
    WeekDays, ClosingPrices = np.loadtxt(
        filename, delimiter=',', usecols=(1, 6),
        unpack=True, converters={1: dmy2Weekday})
    return WeekDays, ClosingPrices


def CalcAveragePrices(WeekDays, ClosingPrices):
    # WeekDays = [4. 0. 1. 2. 3. 4. 0. 1. 2. 3. 4. 0. 1. 2. 3. 4. 1. 2. 3. 4. 0. 1. 2. 3.
    # 4. 0. 1. 2. 3. 4.]
    AveragePrices = np.zeros(5)
    for WeekFay in range(AveragePrices.size): #0 1 2 3 4 5
        AveragePrices[WeekFay] = np.take(
            ClosingPrices,
            np.where(WeekDays == WeekFay)).mean()
    #     print(np.where(WeekDays == WeekFay))
    #     (array([ 1,  6, 11, 20, 25], dtype=int64),)
    #     (array([ 2,  7, 12, 16, 21, 26], dtype=int64),)
    #     (array([ 3,  8, 13, 17, 22, 27], dtype=int64),)
    #     (array([ 4,  9, 14, 18, 23, 28], dtype=int64),)
    #     (array([ 0,  5, 10, 15, 19, 24, 29], dtype=int64),)
    # print(AveragePrices)  [351.79       350.635      352.13666667 350.89833333 350.02285714]
    return AveragePrices


def main(argc, argv, envp):
    WeekDays, ClosingPrices = ReadData('aapl.csv')
    AveragePrices = CalcAveragePrices(
        WeekDays, ClosingPrices)
    MaxIndex = np.argmax(AveragePrices)
    MinIndex = np.argmin(AveragePrices)
    for WeekFay, average_price in enumerate(
            AveragePrices):
        print(G_WeekDays[WeekFay], ':', average_price,
              '(max)' if (WeekFay == MaxIndex) else
              '(min)' if (WeekFay == MinIndex) else '')
    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
