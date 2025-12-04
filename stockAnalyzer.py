import yfinance as yf

def etractbasicInfo (data):
    keysToExtract = ['longName','website','sector','fullTimeEmployees', 'marketCap', 'totalCash', 'trailingEps' ]
    basicInfo = {}
    for key in keysToExtract:
        if key in data:
            basicInfo[key] = data[key]
        else:
            basicInfo[key] = ''
    return basicInfo

    


def getCompanystockInfo (TickerSymbol):

    company = yf.Ticker(TickerSymbol)
    basicinfo = etractbasicInfo(company.info)
    print(basicinfo)

getCompanystockInfo('MSFT')