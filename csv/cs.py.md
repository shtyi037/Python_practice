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
    自行定義日月年
    '''
    return dt.datetime.strptime(str(dmy, encoding='utf-8'),'%d-%m-%Y').date().strftime('%Y-%m-%d')

#converters 轉換器
def read_data(filename):
    dates, opening_prices, highest_prices, \
    lowest_prices, closing_prices = np.loadtxt(
        filename,delimiter=',',
        usecols=(1,3,4,5,6),
        unpack=True,
        dtype=np.dtype('M8[D], f8, f8, f8, f8'),
        converters={1: dmy2ymd})
    print(dates)

def main(argc, argv, envp):
    read_data('aapl.csv')
    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))

```