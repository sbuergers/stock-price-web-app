from flask import Flask, render_template, request, redirect
from alpha_vantage.timeseries import TimeSeries

app = Flask(__name__)


key = 'KX6JA5U3JFVOOYL9'
ts = TimeSeries(key)
aapl, meta = ts.get_daily(symbol='AAPL')
print(aapl['2019-09-12'])

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507)
