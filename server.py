from flask import Flask, abort, request
from stockAnalyzer import getCompanystockInfo
from analyze import analyzeAticle
from flask_cors import CORS
import json

f = open("./test/data.json")
stockTest = json.load(f)


app = Flask(__name__)
CORS(app)


@app.route('/health', methods= ['GET'])
def helloWorld():
    return 'Flask server is running'

@app.route('/analyze-stock/<ticker>', methods= ['GET'])
def analyzeStock(ticker):
    return stockTest
    if  (len(ticker) > 5 or not ticker.isidentifier()):
        abort(400, 'Invalid ticker format')
    try:
        analyze = getCompanystockInfo(ticker)
    except NameError as e:
        abort(404, e)
    except:
        abort(500, 'Something went wrong with your stock analysis')
    return analyze

@app.route('/analyze-Text/', methods= ['POST'])
def analyzeTextHandler():
    data = request.get_json()
    if "text"not in data or not data['text']:
        abort(400, 'No text provided to analyze')
    analysis = analyzeAticle(data['text'])
    return analysis

if __name__ == '__main__':


    app.run(host='0.0.0.0')

