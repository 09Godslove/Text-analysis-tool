import yfinance as yf
import requests, json
from datetime import datetime
from bs4 import BeautifulSoup
import analyze

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

def extractArticleTestFromHTML(soup):
    allText = ''
    result = soup.find_all("div", class_=["body", "post-content", "article-body", "single-post-content"])
    for res in result:
        allText += res.text
    return allText
def extarctNewsarticles(NewsArticles):
    allArticleText = ''
    for Article in NewsArticles:
        url = Article['link']
        if "barrons.com" not in url or "wsj.com" not in url:
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')
        allArticleText += extractArticleTestFromHTML(soup)
    return allArticleText
    

def getCompanystockInfo (TickerSymbol):
    # get data from yahoo finance
    company = yf.Ticker(TickerSymbol)

    # collect all basic info
    basicinfo = etractbasicInfo(company.info) 
    PriceHistory = getStockhistory(company)
    futureEarningDates = getEarningDates(company)
    newsArticles = getNews(company)
    allNewsArticleText = extarctNewsarticles(newsArticles)
    # print(allNewsArticleText)
    finalResult = analyze.analyzeAticle(allNewsArticleText)
    companyStockAnalysisResult = {
        'basicinfo': basicinfo,
        'PriceHistory': PriceHistory,
        'futureEarningDates':futureEarningDates,
        'newsArticles':newsArticles,
        'finalResult':finalResult
    }
    return companyStockAnalysisResult

# StickInnfo = getCompanystockInfo('MSFT')
# print(json.dumps(StickInnfo, indent=4))


