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
    dates, closing_prices = np.loadtxt(
        filename, delimiter=',', usecols=(1, 6),
        unpack=True, dtype=np.dtype('M8[D], f8'),
        converters={1: dmy2ymd})
    return dates, closing_prices


def calc_returns(closing_prices):
    return np.diff(closing_prices) / closing_prices[:-1]


def calc_corr(bhp_returns, vale_returns):
    corr = np.corrcoef(bhp_returns, vale_returns)
    return corr


def manu_corr(bhp_returns, vale_returns):
    ave_a = np.mean(bhp_returns)
    dev_a = bhp_returns - ave_a
    var_a = np.mean(dev_a * dev_a)
    std_a = np.sqrt(var_a)
    ave_b = np.mean(vale_returns)
    dev_b = vale_returns - ave_b
    var_b = np.mean(dev_b * dev_b)
    std_b = np.sqrt(var_b)
    cov_aa = var_a
    cov_ab = np.mean(dev_a * dev_b)
    cov_ba = np.mean(dev_b * dev_a)
    cov_bb = var_b
    covs = np.array([
        [cov_aa, cov_ab],
        [cov_ba, cov_bb]])
    stds = np.array([
        [std_a * std_a, std_a * std_b],
        [std_b * std_a, std_b * std_b]])
    corr = covs / stds
    return corr


def semi_corr(bhp_returns, vale_returns):
    std_a = np.std(bhp_returns, ddof=1)
    std_b = np.std(vale_returns, ddof=1)
    covs = np.cov(bhp_returns, vale_returns)
    stds = np.array([
        [std_a * std_a, std_a * std_b],
        [std_b * std_a, std_b * std_b]])
    corr = covs / stds
    return corr


def init_chart(first_day, last_day):
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.title('Correlation Of Returns', fontsize=20)
    mp.xlabel('Trading Days From %s To %s' % (
        first_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y'),
        last_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y')), fontsize=14)
    mp.ylabel('Returns Of Stock Price', fontsize=14)
    ax = mp.gca()
    ax.xaxis.set_major_locator(
        md.WeekdayLocator(byweekday=md.MO))
    ax.xaxis.set_minor_locator(md.DayLocator())
    ax.xaxis.set_major_formatter(
        md.DateFormatter('%d %b %Y'))

    mp.tick_params(which='both', top=True, right=True,
                   labelright=True, labelsize=10)
    mp.grid(linestyle=':')


def draw_bhp_returns(dates, returns):
    dates = dates.astype(md.datetime.datetime)
    mp.plot(dates, returns, 'o-', c='orangered',
            label='BHP')


def draw_vale_returns(dates, returns):
    dates = dates.astype(md.datetime.datetime)
    mp.plot(dates, returns, 'o-', c='limegreen',
            label='VALE')
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
    dates, bhp_closing_prices = read_data('bhp.csv')
    dates, vale_closing_prices = read_data('vale.csv')
    bhp_returns = calc_returns(bhp_closing_prices)
    vale_returns = calc_returns(vale_closing_prices)
    corr = calc_corr(bhp_returns, vale_returns)
    print(corr)
    corr = manu_corr(bhp_returns, vale_returns)
    print(corr)
    corr = semi_corr(bhp_returns, vale_returns)
    print(corr)
    init_chart(dates[0], dates[-2])
    draw_bhp_returns(dates[:-1], bhp_returns)
    draw_vale_returns(dates[:-1], vale_returns)
    show_chart()
    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
