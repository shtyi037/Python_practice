import os
import sys
import platform
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as mp
import matplotlib.dates as md


def dmy2ymd(dmy):
    return dt.datetime.strptime(str(dmy, encoding='utf-8'),
        '%d-%m-%Y').date().strftime('%Y-%m-%d')


def ReadData(filename):
    dates, opening_prices, HighestPrices, \
        LowestPrices, ClosingPrices = np.loadtxt(
            filename, delimiter=',',
            usecols=(1, 3, 4, 5, 6), unpack=True,
            dtype=np.dtype('M8[D], f8, f8, f8, f8'),
            converters={1: dmy2ymd})
    return dates, opening_prices, HighestPrices, LowestPrices, ClosingPrices


def CalcPivots(HighestPrices, LowestPrices,ClosingPrices):
    '''
    計算基準位
    '''
    pivots = (HighestPrices + LowestPrices +ClosingPrices) / 3 #取平均
    spreads = HighestPrices - LowestPrices #每天價差
    supports = pivots - spreads #支撐位
    resistances = pivots + spreads #壓力位
    return pivots, supports, resistances


def FitLine(fitX, fitY, lineX):
    ones = np.ones_like(fitX)
    a = np.vstack([fitX, ones]).T
    b = fitY
    x = np.linalg.lstsq(a, b)[0]
    k, b = x[0], x[1]
    lineY = k * lineX + b
    return lineY


def InitChart(FirstDay, LastDay):
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.title('Trend Line', fontsize=20)
    mp.xlabel('Trading Days From %s To %s' % (
        FirstDay.astype(md.datetime.datetime).strftime('%d %b %Y'),
        LastDay.astype(md.datetime.datetime).strftime('%d %b %Y')), fontsize=14)
    mp.ylabel('Stock Price (USD) Of Apple Inc.',fontsize=14)
    ax = mp.gca()
    ax.xaxis.set_major_locator(
        md.WeekdayLocator(byweekday=md.MO))
    ax.xaxis.set_minor_locator(md.DayLocator())
    ax.xaxis.set_major_formatter(md.DateFormatter('%d %b %Y'))

    mp.tick_params(which='both', top=True, right=True,labelright=True, labelsize=10)
    mp.grid(linestyle=':')


def DrawCandlestick(
        dates, opening_prices, HighestPrices,
        LowestPrices, ClosingPrices):
    dates = dates.astype(md.datetime.datetime)
    up = ClosingPrices - opening_prices >= 1e-2
    down = opening_prices - ClosingPrices >= 1e-2
    fc = np.zeros(dates.size, dtype='3f4')
    ec = np.zeros(dates.size, dtype='3f4')
    fc[up], fc[down] = (1, 1, 1), (0.85, 0.85, 0.85) #將顏色改灰色
    ec[up], ec[down] = (0.85, 0.85, 0.85), (0.85, 0.85, 0.85) 
    mp.bar(dates, HighestPrices - LowestPrices, 0,
           LowestPrices, align='center', color=fc,edgecolor=ec)
    mp.bar(dates, ClosingPrices - opening_prices, 0.8,
           opening_prices, align='center', color=fc,edgecolor=ec)
    mp.gcf().autofmt_xdate()


def DrawPivots(dates, pivots, supports, resistances):
    dates = dates.astype(md.datetime.datetime)
    mp.plot(dates, pivots, 's', c='dodgerblue',label='Pivot')
    mp.plot(dates, supports, 's', c='limegreen',label='Support')
    mp.plot(dates, resistances, 's', c='orangered',label='Resistance')


def DrawTrendLine(dates, predays, trend_line):
    '''
    畫出趨勢線
    '''
    dates = dates.astype(md.datetime.datetime)
    mp.plot(
        dates[:-predays], trend_line[:-predays],'o-', 
        c='dodgerblue', linewidth=3,label='Trend Line')
    mp.plot(
        dates[-predays - 1:], trend_line[-predays - 1:],'o:',
        c='dodgerblue', linewidth=3)


def DrawSupportLine(dates, predays, support_line):
    '''
    畫出支撐線
    '''
    dates = dates.astype(md.datetime.datetime)
    mp.plot(
        dates[:-predays], support_line[:-predays],'o-',
        c='limegreen', linewidth=3,label='Support Line')
    mp.plot(
        dates[-predays - 1:], support_line[-predays - 1:],'o:',
         c='limegreen', linewidth=3)


def DrawResistanceLine(dates, predays, resistance_line):
    '''
    畫出阻力線(壓力線)
    '''
    dates = dates.astype(md.datetime.datetime)
    mp.plot(
        dates[:-predays], resistance_line[:-predays],'o-',
         c='orangered', linewidth=3,label='Resistance Line')
    mp.plot(
        dates[-predays - 1:], resistance_line[-predays - 1:],'o:',
         c='orangered', linewidth=3)


def ShowChart():
    mng = mp.get_current_fig_manager()
    if 'Windows' in platform.system():
        mng.window.state('zoomed')
    else:
        mng.resize(*mng.window.maxsize())
    mp.show()


def main(argc, argv, envp):
    dates, opening_prices, HighestPrices, \
        LowestPrices, ClosingPrices = ReadData(
            'aapl.csv')
    pivots, supports, resistances = CalcPivots(
        HighestPrices, LowestPrices, ClosingPrices)
    predays = 5 #預測天數
    for i in range(predays):
        dates = np.append(dates, np.datetime64(
            (pd.to_datetime(str(dates[-1])).date() +
             pd.tseries.offsets.BDay()).strftime('%Y-%m-%d'),'D'))
    print(dates)
    days = dates.astype(int)
    trend_line = FitLine(days[:-predays], pivots, days)
    support_line = FitLine(days[:-predays], supports, days)
    resistance_line = FitLine(days[:-predays], resistances, days)
    InitChart(dates[0], dates[-1])
    DrawCandlestick(
        dates[:-predays], opening_prices, HighestPrices,
        LowestPrices, ClosingPrices)
    DrawPivots(dates[:-predays], pivots, supports, resistances)
    DrawTrendLine(dates, predays, trend_line)
    DrawSupportLine(dates, predays, support_line)
    DrawResistanceLine(dates, predays, resistance_line)
    ShowChart()
    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
