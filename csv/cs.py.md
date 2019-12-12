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
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255) #底色
    mp.title('Candlestick Chart', fontsize=23) #標題內容和字體大小
    #設定x軸向字串'Trading Days From 第一天日期 To 最後一天日期'
    mp.xlabel('Trading Days From %s To %s' % (
        first_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y'),
        last_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y')), fontsize=15)
    #設定y軸向字串(直)
    mp.ylabel('Stock Price (USD) Of Apple Inc.',fontsize=17)

    #取軸
    ax = mp.gca()
    ax.xaxis.set_major_locator(md.WeekdayLocator(byweekday=md.MO))#周一
    ax.xaxis.set_minor_locator(md.DayLocator())
    ax.xaxis.set_major_formatter(md.DateFormatter('%d %b %Y'))#日期格式

    mp.tick_params(which='both', top=True, right=True, labelright=True, labelsize=11)#刻度
    mp.grid(linestyle=':')


def show_chart():
    mng = mp.get_current_fig_manager() #獲取當前圖表管理器
    if 'Windows' in platform.system(): #獲取當前電腦的系統
        mng.window.state('zoomed') #如果是windows則最大化
    else:
        mng.resize(*mng.window.maxsize())#修改大小,改為最大
    mp.show()

def draw_chart(dates, opening_prices, highest_prices,lowest_prices, closing_prices):
    dates = dates.astype(md.datetime.datetime)

    up = closing_prices - opening_prices >= 1e-2 # 0.01 美元 =1*0.01
    down = opening_prices - closing_prices >= 1e-2

    fc = np.zeros(dates.size, dtype='3f4')
    ec = np.zeros(dates.size, dtype='3f4')
    
    fc[up], fc[down] = (1, 1, 1), (0, 0.5, 0)
    ec[up], ec[down] = (1, 0, 0), (0, 0.5, 0)

    mp.bar(dates, highest_prices - lowest_prices, 0,
           lowest_prices, align='center', color=fc,
           edgecolor=ec)#收盤-開盤
    mp.bar(dates, closing_prices - opening_prices, 0.8,
           opening_prices, align='center', color=fc,
           edgecolor=ec)#最高價減最低價
    
    mp.gcf().autofmt_xdate()#水平方向的日期自動做調整,圖變小後日期不會重疊

def main(argc, argv, envp):
    dates, opening_prices, highest_prices, lowest_prices, closing_prices = \
    read_data('aapl.csv')
    
    init_chart(dates[0], dates[-1])#傳入第一天與最後一天
    draw_chart(dates, opening_prices, highest_prices,lowest_prices, closing_prices)
    show_chart()
    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))

```