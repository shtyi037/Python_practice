import os
import sys
import numpy as np


def ReadData(filename):
    dates, HighestPrices, LowestPrices, \
        ClosingPrices = np.loadtxt(
            filename, delimiter=',', usecols=(1, 4, 5, 6),
            unpack=True, dtype=np.dtype('U10, f8, f8, f8'))
    return dates, HighestPrices, LowestPrices, \
        ClosingPrices


def TrueRange(HighestPrices, LowestPrices,
               ClosingPrices):
    hc = HighestPrices - ClosingPrices #當日最高價-前日收盤價
    cl = ClosingPrices - LowestPrices #前日收盤價-當日最低價
    hl = HighestPrices - LowestPrices #當日最高價-當日最低價
    tr = np.maximum(np.maximum(hc, cl), hl) #多個數組中找最大的
    return tr


def AverageTrueRange(tr):
    '''
    平均真實波幅:
    ATR[i]=(ATR[i-1]x(N-1)+TR[i])/N, i=1,2,...,N-1
    '''
    atr = np.zeros(tr.size)
    for i in range(atr.size):
        atr[i] = tr.mean() if i == 0 else (
            atr[i - 1] * (tr.size - 1) + tr[i]) / tr.size
    return atr


def ShowAtr(dates, atr):
    for i, date in enumerate(dates[1:]):
        print(date, atr[i])


def main(argc, argv, envp):
    dates, HighestPrices, LowestPrices, \
        ClosingPrices = ReadData('檔案名.csv')
    N = 20
    dates = dates[-N - 1:]
    HighestPrices = HighestPrices[-N:]
    LowestPrices = LowestPrices[-N:]
    ClosingPrices = ClosingPrices[-N - 1:-1]
    tr = TrueRange(HighestPrices, LowestPrices,ClosingPrices)
    atr = AverageTrueRange(tr)
    ShowAtr(dates, atr)
    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
