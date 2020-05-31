from flask import Flask, render_template, request, redirect

# Get environment variables (API key)
import os

# Data handling
import pandas as pd
import json

# Stock data API
from alpha_vantage.timeseries import TimeSeries

# Data visualization
import bokeh
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource


app = Flask(__name__)



# Given User search of stock name/id, retrieve data from alpha vantage
# Default is AAPL (Apple Inc.)
def query_stock(stock_id='aapl'):
	
	## Get stock data
	key = os.environ["ALPHA_VANTAGE_KEY"]
	ts = TimeSeries(key)
	data, meta = ts.get_daily(symbol=stock_id)
	
	## Convert to pandas DataFrame
	df = pd.DataFrame(data).transpose()
	
	## Make sure dates are of type datetime
	df.index = pd.to_datetime(df.index)
	df.index.name = 'date'
	
	## Change columns names
	df.rename(columns={'1. open':'open',
	                   '2. high':'high',
	                   '3. low':'low',
					   '4. close':'close',
					   '5. volume':'volume'}, 
	                 inplace=True)
	return df


# Creates interactive time-series plot of stock prices given data in df
def make_plot(df):
	source = ColumnDataSource(df)
	p = figure(x_axis_type="datetime", plot_width=800, plot_height=350)
	p.line('date', 'close', source=source)
	p.xaxis.axis_label = 'Date'
	p.yaxis.axis_label = 'Price (closing)'
	hover = HoverTool(
	    tooltips=[
	        ('date', '@date{%F}'),
	        ('close', '@close{$%0.2f}'), 
	        ('volume', '@volume{0.00 a}'),
	    ],
	    formatters={
	        '@date' : 'datetime', 
	        '@close': 'printf',   
	    },
	    mode='vline'
	)
	p.add_tools(hover)
	return p


# give Bokeh plot elements for curren stock
def plot(stock):
	df = query_stock(stock)
	p = make_plot(df)
	script, div = components(p)
	return script, div


# Initial page (showing apple stock)
@app.route('/')
def root():
	stock = 'aapl'
	plots = []
	plots.append(plot(stock))
	return render_template('index.html', plots=plots)


# User searches for stock
@app.route('/search', methods=['POST', 'GET'])
def search_stock():
	if request.method == 'POST':
		searchterm = request.form.get('search')
		if searchterm:
			try:
				stock = searchterm.lower()
				plots = []
				plots.append(plot(stock))
				return render_template('index.html', plots=plots)
			except:
				return render_template('limitreached.html')
		else:
			return render_template('notfound.html')
	else:
		redirect('/')


if __name__ == '__main__':
  app.run(port=33507)
