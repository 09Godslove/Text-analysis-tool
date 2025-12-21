from flask import Flask, abort
from stockAnalyzer import getCompanystockInfo


app = Flask(__name__)



@app.route('/health')
def helloWorld():
    return 'Flask server is running'

@app.route('/analyze-stock/<ticker>')
def analyzeStock(ticker):
    if  (len(ticker) > 5 or not ticker.isidentifier()):
        abort(400, 'Invalid ticker format')
    try:
        analyze = getCompanystockInfo(ticker)
    except NameError as e:
        abort(404, e)
    except:
        abort(500, 'Something went wrong with your stock analysis')
    return analyze

if __name__ == '__main__':


    app.run()

