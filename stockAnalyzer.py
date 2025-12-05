import yfinance as yf
import requests
from datetime import datetime

def etractbasicInfo (data):
    keysToExtract = ['longName','website','sector','fullTimeEmployees', 'marketCap', 'totalCash', 'trailingEps' ]
    basicInfo = {}
    for key in keysToExtract:
        if key in data:
            basicInfo[key] = data[key]
        else:
            basicInfo[key] = ''
    return basicInfo

    
def getStockhistory(company):
    hst = company.history(period='12mo')
    prices = hst["Open"].tolist()
    dates = hst.index.strftime('%Y-%m-%d').tolist()
    return {
        'Price': prices,
        'Date': dates
    }

def getEarningDates(company):
    earningDatedf = company.earnings_dates
    allDates = earningDatedf.index.strftime('%Y-%m-%d').tolist()
    dateObjects = [datetime.strptime(date, '%Y-%m-%d') for date in allDates]
    currentDate = datetime.now()
    futureDates = [date.strftime('%Y-%m-%d') for date in dateObjects if date >currentDate]
    return futureDates
def getNews(company):
    newsList = company.news
    allNewsArticles = []
    for newsdict in newsList:
        content = newsdict.get("content", {})

        newsDictToAdd = {
            "title": content.get("title"),
            "link": content.get("canonicalUrl", {}).get("url")
        }
        allNewsArticles.append(newsDictToAdd)
    return allNewsArticles
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
def extarctNewsarticles(NewsArticles):
    url = NewsArticles[0]['link']
    page = requests.get(url, headers=headers)
    print(page.text)

def getCompanystockInfo (TickerSymbol):
    # get data from yahoo finance
    company = yf.Ticker(TickerSymbol)

    # collect all basic info
    basicinfo = etractbasicInfo(company.info) 
    PriceHistory = getStockhistory(company)
    futureEarningDates = getEarningDates(company)
    newsArticles = getNews(company)
    extarctNewsarticles(newsArticles)

getCompanystockInfo('MSFT')