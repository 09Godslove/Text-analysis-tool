from flask import Flask, abort


app = Flask(__name__)



@app.route('/health')
def helloWorld():
    return 'Flask server is running'

@app.route('/analyze-stock/<ticker>')
def analyzeStock(ticker):
    if  (len(ticker) > 5 or not ticker.isidentifier()):
        abort(400, 'Invalid ticker format')
    return{
        'data': 'Analysis for ' + ticker + ' is ongoing'
    }


if __name__ == '__main__':


    app.run()

