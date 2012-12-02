# Library for Interacting with Yahoo Datafeed.
import urllib2 as url
import pandas as pd

def __request(symbol, stat):
    address = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    return url.urlopen(address).read().strip().strip('"')

def __convert(string):
    if string[-1] == 'B' or string [-1] == 'b':
        return float(string[0:-1])*1000000000.0
    elif string[-1] == 'M' or string[-1] == 'm':
        return float(string[0:-1])*1000000.0
    return

def get_all(symbol):
    data = {}
    data['price'] = get_price(symbol)
    data['change']= get_change(symbol)
    data['volume'] = get_volume(symbol)
    data['avg_daily_volume'] = get_avg_daily_volume(symbol)
    data['stock_exchange'] = get_stock_exchange(symbol)
    data['market_cap'] = get_market_cap(symbol)
    data['book_value'] = get_book_value(symbol)
    data['ebitda'] = get_ebitda(symbol)
    data['dividend_per_share'] = get_dividend_per_share(symbol)
    data['dividend_yield'] = get_dividend_yield(symbol)
    data['earnings_per_share'] = get_earnings_per_share(symbol)
    data['52_week_high'] = get_52_week_high(symbol)
    data['52_week_low'] = get_52_week_low(symbol)
    data['50day_moving_avg'] = get_50day_moving_avg(symbol)
    data['200day_moving_avg'] = get_200day_moving_avg(symbol)
    data['price_earnings_ratio'] = get_price_earnings_ratio(symbol)
    data['price_earnings_growth_ratio'] = get_price_earnings_growth_ratio(symbol)
    data['price_sales_ratio'] = get_price_sales_ratio(symbol)
    data['price_book_ratio'] = get_price_book_ratio(symbol)
    data['short_ratio'] = get_short_ratio(symbol)
    return pd.Series(data)

def get_all_rt(symbol):
    dat = {}
    return pd.Series(data)

def get_price(symbol):
    return float(__request(symbol, 'l1'))

def get_change(symbol):
    return float(__request(symbol, 'c1'))

def get_volume(symbol):
    return float(__request(symbol, 'v'))

def get_avg_daily_volume(symbol):
    return float(__request(symbol, 'a2'))

def get_stock_exchange(symbol):
    return __request(symbol, 'x')

def get_market_cap(symbol):
    return __convert(__request(symbol, 'j1'))

def get_book_value(symbol):
    return float(__request(symbol, 'b4'))

def get_ebitda(symbol): 
    return __convert(__request(symbol, 'j4'))
    
def get_dividend_per_share(symbol):
    return float(__request(symbol, 'd'))

def get_dividend_yield(symbol): 
    return float(__request(symbol, 'y'))
    
def get_earnings_per_share(symbol): 
    return float(__request(symbol, 'e'))

def get_52_week_high(symbol): 
    return float(__request(symbol, 'k'))
    
def get_52_week_low(symbol): 
    return float(__request(symbol, 'j'))

def get_50day_moving_avg(symbol): 
    return float(__request(symbol, 'm3'))
    
def get_200day_moving_avg(symbol): 
    return float(__request(symbol, 'm4'))
    
def get_price_earnings_ratio(symbol): 
    return float(__request(symbol, 'r'))

def get_price_earnings_growth_ratio(symbol): 
    return float(__request(symbol, 'r5'))

def get_price_sales_ratio(symbol): 
    return float(__request(symbol, 'p5'))
    
def get_price_book_ratio(symbol): 
    return float(__request(symbol, 'p6'))
       
def get_short_ratio(symbol): 
    return float(__request(symbol, 's7'))

# NEW PROPERTIES

# Real Time
def get_after_hrs_change(symbol):
    return float(__request(symbol, 'c8'))

def get_annualized_gain(symbol):
    return float(__request(symbol, 'g3'))

def get_ask(symbol):
    return float(__request(symbol, 'a0'))

# Real Time
def get_ask_rt(symbol):
    return float(__request(symbol, 'b2'))

def get_ask_size(symbol):
    return float(__request(symbol, 'a5'))

def get_bid(symbol):
    return float(__request(symbol, 'b0'))

# Real Time
def get_bid_rt(symbol):
    return float(__request(symbol, 'b3'))

def get_bid_size(symbol):
    return float(__request(symbol, 'b6'))

# insert Book Value Per Share, Change, Change Change in Percent, Change from 50 Day MA, Change from 200 day MA, Change from Year High, Change from Year Low, Change in Percent

# Real Time
def get_change_in_percent_rt(symbol):
    return float(__request(symbol, 'k2'))

def get_change_rt(symbol):
    return float(__request(symbol, 'c6'))
    
def get_historical_prices_csv(symbol, start_date, end_date):
    address = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'a=%s&' % str(int(start_date[4:6]) - 1) + \
          'b=%s&' % str(int(start_date[6:8])) + \
          'c=%s&' % str(int(start_date[0:4])) + \
          'd=%s&' % str(int(end_date[4:6]) - 1) + \
          'e=%s&' % str(int(end_date[6:8])) + \
          'f=%s&' % str(int(end_date[0:4])) + \
          'g=d&ignore=.csv'
    return url.urlopen(address).read()
    
def get_historical_prices(symbol, start_date, end_date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    
    Returns a pandas dataframe
    """

    address = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'a=%s&' % str(int(start_date[4:6]) - 1) + \
          'b=%s&' % str(int(start_date[6:8])) + \
          'c=%s&' % str(int(start_date[0:4])) + \
          'd=%s&' % str(int(end_date[4:6]) - 1) + \
          'e=%s&' % str(int(end_date[6:8])) + \
          'f=%s&' % str(int(end_date[0:4])) + \
          'g=d&ignore=.csv'

    return pd.read_csv(address, index_col = 0, parse_dates = True).sort()

def dfTwoYearClose(symbol):
    df = get_historical_prices(symbol, '20100101', '20120101')
    return df['Adj Close']

def dfOneMonthClose(symbol):
    df = get_historical_prices(symbol, '20120101', '20120201')
    return df['Adj Close']
