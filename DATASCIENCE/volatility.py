import os
import sys
import numpy as np


def ReadData(filename):
    ClosingPrices = np.loadtxt(filename, delimiter=',', usecols=(6), unpack=True)
    return ClosingPrices


def CalcVolatility(ClosingPrices):
    LogClosingPrices = np.log(ClosingPrices)
    LogRets = np.diff(LogClosingPrices)
    LogRets_std = np.std(LogRets)
    Volatility = LogRets_std / LogRets.mean() / \
        np.sqrt(1 / 252)
    return Volatility


def main(argc, argv, envp):
    ClosingPrices = ReadData('檔案名.csv')
    Volatility = CalcVolatility(ClosingPrices)
    print(Volatility)
    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
