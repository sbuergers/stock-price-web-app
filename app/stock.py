'''
Using the alpha vantage API get stock prices of the day
'''
# Get environment variables (API key)
import os

# Data handling
import pandas as pd

# Stock data API
from alpha_vantage.timeseries import TimeSeries

# Data visualization
import bokeh
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource,

# Date-time handling
import datetime


## Company name dictionary
company = {'aapl':'Apple Inc.'}


## Input of stock data
## TODO
stock_id = 'aapl'
ylabel = 'Price (closing)'
xlabel = 'Date'

## Get stock data
key = os.environ("ALPHA_VANTAGE_KEY")
ts = TimeSeries(key)
data, meta = ts.get_daily(symbol=stock_id)
print(data['2020-01-07'])

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


## Bokeh visualization
source = ColumnDataSource(df)

p = figure(x_axis_type="datetime", 
		   plot_width=800, plot_height=350)
p.line('date', 'close', source=source)
p.xaxis.axis_label = xlabel
p.yaxis.axis_label = ylabel

HoverTool(
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
output_file("time_series.html")
show(p)







# eof