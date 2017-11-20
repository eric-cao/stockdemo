
import MySQLdb

import requests  # interaction with the web
import os  # file system operations
import yaml  # human-friendly data format
import re  # regular expressions
import pandas as pd  # pandas... the best time series library out there
import datetime as dt  # date and time functions
import io
from datetime import timedelta

# from .extra import ProgressBar

dateTimeFormat = "%Y%m%d %H:%M:%S"


def getSymbolData(symbol, sDate=(2000, 1, 1), adjust=False, verbose=True):
    """
    get data from Yahoo finance and return pandas dataframe

    Parameters
    -----------
    symbol : str
        Yahoo finanance symbol
    sDate : tuple , optional
        start date (y,m,d), defaults to 1 jan 1990
    adjust : bool , optional
        use adjusted close values to correct OHLC. adj_close will be ommited
    verbose : bool , optional
        print output

    Returns
    ---------
        DataFrame

    """

    period1 = int(dt.datetime(*sDate).timestamp())  # convert to seconds since epoch
    period2 = int(dt.datetime.now().timestamp())

    params = (symbol, period1, period2, _token['crumb'])

    url = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&crumb={3}".format(
        *params)

    print(url)
    data = requests.get(url, cookies={'B': _token['cookie']})

    buf = io.StringIO(data.text)  # create a buffer
    df = pd.read_csv(buf, index_col=0, parse_dates=True)  # convert to pandas DataFrame

    # rename columns
    newNames = [c.lower().replace(' ', '_') for c in df.columns]
    renames = dict(zip(df.columns, newNames))
    df = df.rename(columns=renames)

    if verbose:
        print(('Got %i days of data' % len(df)))

    if adjust:
        return _adjust(df, removeOrig=True)
    else:
        return df


def _adjust(df, removeOrig=False):
    '''
  _adjustust hist data based on adj_close field
    '''
    c = df['close'] / df['adj_close']

    df['adj_open'] = df['open'] / c
    df['adj_high'] = df['high'] / c
    df['adj_low'] = df['low'] / c

    if removeOrig:
        df = df.drop(['open', 'close', 'high', 'low'], axis=1)
        renames = dict(list(zip(['adj_open', 'adj_close', 'adj_high', 'adj_low'], ['open', 'close', 'high', 'low'])))
        df = df.rename(columns=renames)

    return df


def loadToken():
    """
    get cookie and crumb from APPL page or disk.
    force = overwrite disk data
    """
    refreshDays = 30  # refreh cookie every x days

    # set destinatioin file
    dataDir = os.path.expanduser('~') + '/twpData'
    dataFile = dataFile = os.path.join(dataDir, 'yahoo_cookie.yml')

    try:  # load file from disk

        data = yaml.load(open(dataFile, 'r'))
        age = (dt.datetime.now() - dt.datetime.strptime(data['timestamp'], dateTimeFormat)).days
        assert age < refreshDays, 'cookie too old'

    except (AssertionError, FileNotFoundError):  # file not found

        if not os.path.exists(dataDir):
            os.mkdir(dataDir)

        data = getToken(dataFile)

    return data


def getToken(fName=None):
    """ get cookie and crumb from yahoo """

    url = 'https://uk.finance.yahoo.com/quote/AAPL/history'  # url for a ticker symbol, with a download link
    r = requests.get(url)  # download page

    txt = r.text  # extract html

    cookie = r.cookies['B']  # the cooke we're looking for is named 'B'

    pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')

    for line in txt.splitlines():
        m = pattern.match(line)
        if m is not None:
            crumb = m.groupdict()['crumb']

    assert r.status_code == 200  # check for succesful download

    # save to disk
    data = {'crumb': crumb, 'cookie': cookie, 'timestamp': dt.datetime.now().strftime(dateTimeFormat)}

    if fName is not None:  # save to file
        with open(fName, 'w') as fid:
            yaml.dump(data, fid)

    return data


# -------------- get token
_token = loadToken()  # get token from disk or yahoo



stockSymbol = 'GOOGL';

# get the latest stock info
# to get the history, set the sDate = (2010,1,1) as history date

processDay = (dt.datetime.today() - timedelta(days=1))

sDate = (processDay.year,processDay.month,processDay.day)
# sDate = (2010, 1, 1)
print(sDate)


result = getSymbolData(stockSymbol,sDate)

#
conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="root",
                  db="stocks")
x = conn.cursor()


# print (result)
try:
    for index, row in result.iterrows():
        x.execute(
            """INSERT INTO stock_detail (symbol,date,open,close,low,high,adj_close,volume) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (stockSymbol,index,row['open'],row['close'],row['low'],row['high'],row['adj_close'],row['volume']))
    conn.commit()
    print('commit -----')
except Exception as e:
    print(e)
    conn.rollback()
    print('rollback -----')

conn.close()