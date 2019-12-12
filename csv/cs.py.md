# cs.py
```python=
import os
import sys
import platform
import datetime as dt
import numpy as np
import matplotlib.pyplot as mp
import matplotlib.dates as md


#strptime 解析
#strftime
def dmy2ymd(dmy):
    '''
    自行定義年-月-日
    '''
    return dt.datetime.strptime(
        str(dmy, encoding='utf-8'),
        '%d-%m-%Y').date().strftime('%Y-%m-%d')
        
#converters 轉換器
def read_data(filename):
    dates, opening_prices, highest_prices, \
    lowest_prices, closing_prices = np.loadtxt(
        filename,delimiter=',',
        usecols=(1,3,4,5,6),
        unpack=True,
        dtype=np.dtype('M8[D], f8, f8, f8, f8'),
        converters={1: dmy2ymd})
    return dates, opening_prices, highest_prices, lowest_prices, closing_prices


def init_chart(first_day, last_day):
    '''
    初始化
    '''
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.title('Candlestick Chart', fontsize=23)#標題內容和字體大小
    #設定x軸向
    mp.xlabel('Trading Days From %s To %s' % (
        first_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y'),
        last_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y')), fontsize=15)
    #設定y軸向(直)
    mp.ylabel('Stock Price (USD) Of Apple Inc.',fontsize=17)

    #取軸
    ax = mp.gca()
    ax.xaxis.set_major_locator(md.WeekdayLocator(byweekday=md.MO))#周一
    ax.xaxis.set_minor_locator(md.DayLocator())
    ax.xaxis.set_major_formatter(md.DateFormatter('%d %b %Y'))#日期格式

    mp.tick_params(which='both', top=True, right=True,labelright=True, labelsize=10)#刻度
    mp.grid(linestyle=':')


def show_chart():
    mp.show()

def main(argc, argv, envp):
    dates, opening_prices, highest_prices, lowest_prices, closing_prices = \
    read_data('aapl.csv')
    
    init_chart(dates[0], dates[-1])
    show_chart()
    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
```