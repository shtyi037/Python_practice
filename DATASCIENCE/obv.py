import os
import sys
import platform
import datetime as dt
import numpy as np
import matplotlib.pyplot as mp
import matplotlib.dates as md


def dmy2ymd(dmy):
    return dt.datetime.strptime(
        str(dmy, encoding='utf-8'),
        '%d-%m-%Y').date().strftime('%Y-%m-%d')


def read_data(filename):
    dates, closing_prices, volumes = np.loadtxt(
        filename, delimiter=',', usecols=(1, 6, 7),
        unpack=True, dtype=np.dtype('M8[D], f8, f8'),
        converters={1: dmy2ymd})
    return dates, closing_prices, volumes


def calc_obvs(closing_prices, volumes):
    diffs = np.diff(closing_prices)
    #signs = np.sign(diffs)
    signs = np.piecewise(diffs,
                         [diffs < 0, diffs == 0, diffs > 0],
                         [-1, 0, 1])
    obvs = volumes[1:] * signs
    return obvs


def init_chart(first_day, last_day):
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.title('On-Balance Volume', fontsize=20)
    mp.xlabel('Trading Days From %s To %s' % (
        first_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y'),
        last_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y')), fontsize=14)
    mp.ylabel('OBV Of BHP', fontsize=14)
    ax = mp.gca()
    ax.xaxis.set_major_locator(
        md.WeekdayLocator(byweekday=md.MO))
    ax.xaxis.set_minor_locator(md.DayLocator())
    ax.xaxis.set_major_formatter(
        md.DateFormatter('%d %b %Y'))

    mp.tick_params(which='both', top=True, right=True,
                   labelright=True, labelsize=10)
    mp.grid(linestyle=':')


def draw_chart(dates, obvs):
    dates = dates.astype(md.datetime.datetime)
    up = obvs > 0
    down = obvs < 0
    fc = np.zeros(dates.size, dtype='3f4')
    ec = np.zeros(dates.size, dtype='3f4')
    fc[up], fc[down] = (1, 0, 0), (0, 0.5, 0)
    ec[up], ec[down] = (1, 1, 1), (1, 1, 1)
    obvs[down] *= -1
    mp.bar(dates, obvs, 1.0, 0, align='center',
           color=fc, edgecolor=ec, label='OBV')
    mp.gcf().autofmt_xdate()
    mp.legend()


def show_chart():
    mng = mp.get_current_fig_manager()
    if 'Windows' in platform.system():
        mng.window.state('zoomed')
    else:
        mng.resize(*mng.window.maxsize())
    mp.show()


def main(argc, argv, envp):
    dates, closing_prices, volumes = read_data('bhp.csv')
    dates = dates[1:]
    obvs = calc_obvs(closing_prices, volumes)
    init_chart(dates[0], dates[-1])
    draw_chart(dates, obvs)
    show_chart()
    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
