from flask import Flask


app = Flask(__name__)



@app.route('/health')
def helloWorld():
    return 'Flask server is running'

@app.route('/analyze-stock/<ticker>')
def analyzeStock(ticker):
    return{
        'data': 'Analysis for ' + ticker + ' is ongoing'
    }


if __name__ == '__main__':


    app.run()

