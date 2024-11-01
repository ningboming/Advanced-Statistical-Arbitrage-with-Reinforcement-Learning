"""download sp500"""
import yfinance as yf
import bs4 as bs
import requests
import datetime

def download_sp500(start_date: datetime.datetime, end_date: datetime.datetime):
    '''
    download sp 500 stocks
    '''
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    tickers = [s.replace('\n', '') for s in tickers]
    data = yf.download(tickers, start=start_date, end=end_date)

    return data

def download_one_stock(name: str, start: str, end: str):
  '''
  name: name of stock 
  start: "2009-01-01" 
  end: "2012-01-01"
  output: adj close prices of the stock
  '''
  data = yf.download(name, start=start, end=end, interval = "1d")
  s = data['Adj Close']
  return s