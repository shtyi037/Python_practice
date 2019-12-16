import os
import sys
import csv
import datetime as dt
import numpy as np


g_weekdays = ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')


def dmy2weekday(dmy):
    '''
    csv檔中,將日期%d-%m-%Y做轉換,
    星期一為0,
    星期二為1,
    ...以此類推到
    '''
    return dt.datetime.strptime(str(dmy, encoding='utf-8'),'%d-%m-%Y').date().weekday()


def read_data(filename):
    weekdays, opening_prices, highest_prices, \
        lowest_prices, closing_prices = np.loadtxt(
            filename, delimiter=',', usecols=(1, 3, 4, 5, 6),
            unpack=True, converters={1: dmy2weekday})
    #此處先處理前15天
    return weekdays[:16], opening_prices[:16], \
        highest_prices[:16], lowest_prices[:16], \
        closing_prices[:16]


def get_summary(
    week_indices, opening_prices, highest_prices,
        lowest_prices, closing_prices):
    opening_price = opening_prices[week_indices[0]]
    highest_price = np.max(np.take(highest_prices, week_indices)) #當周的最高價
    lowest_price = np.min(np.take(lowest_prices, week_indices)) #當周最低價
    closing_price = closing_prices[week_indices[-1]]
    return opening_price, highest_price, lowest_price, closing_price


def get_summaries(
        weekdays, opening_prices, highest_prices,
        lowest_prices, closing_prices):
    '''
    計算三周
    '''
    first = np.where(weekdays == 0)[0][0] #第一天(第一個星期一)
    last = np.where(weekdays == 4)[0][-1] #最後一天(最後一個星期五)
    indices = np.arange(first, last + 1)
    indices = np.split(indices, 3)
    summaries = np.apply_along_axis(
        get_summary, 1, indices, opening_prices,
        highest_prices, lowest_prices, closing_prices)
    print(summaries)
    return summaries


def save_summaries(summaries):
    '''
    將計算出的值儲存檔案
    '''
    filename = '檔案名.csv'
    # np.savetxt(filename, summaries, delimiter=',',fmt='%g')
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for summary in summaries:
            row = list(summary)
            row.insert(0, '自取公司名')
            writer.writerow(row)


def main(argc, argv, envp):
    
    weekdays, opening_prices, highest_prices, \
    lowest_prices, closing_prices = read_data('檔案名.csv') #讀取檔案中的所有值,並存入變數
    #get_summaries函式可回傳多個數組
    summaries = get_summaries(
        weekdays, opening_prices, highest_prices,
        lowest_prices, closing_prices
    )
    # print(summaries)
    save_summaries(summaries) #儲存到csv檔中
    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
