# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 16:16:28 2020

@author: choibosu
"""
import json as json
import requests
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models import DatetimeTickFormatter
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_plot(val1, val2):
    
    str1 = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='
    str2 = '&outputsize=full&datatype=json&apikey=ENECMQ5G9B8I3G11'
    str_full = str1 + val1 + str2
    
    r = requests.get(str_full)
    response = r.json()
    data = pd.DataFrame.from_dict(response['Time Series (Daily)'], orient= 'index').sort_index(axis=1)
    data.reset_index(level=0, inplace=True)
    data = data.rename(columns={'index': 'Date', '1. open': 'Open', '2. high': 'High', '3. low': 'Low',\
                            '4. close': 'Close', '5. adjusted close': 'Adjusted Close', '6. volume': 'Volume'})
    data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume']]
    data['Date'] = pd.to_datetime(data['Date']) 
    df = data.astype({'Open':'float', 'High':'float','Low':'float','Close':'float', 'Adjusted Close':'float',\
                      'Volume':'int32'})
    dft = df[{'Date', val2}]

    source = ColumnDataSource(dft)

    p = figure()
    p.line(source=source, x = 'Date', y = val2)

    p.title.text = 'Daily Stock Price'
    p.xaxis.axis_label = 'Date'
    p.xaxis.formatter = DatetimeTickFormatter(days=['%m/%d'], months=['%m/%Y'], years=['%Y'])
    p.yaxis.axis_label = val2
    
    #html = file_html(p, CDN, "my plot")
    
    #return html
    return p

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/', methods = ['POST'])
def getvalue():
    global result_plot
    Ticker = request.form['ticker']
    Request = request.form['features']
    result_plot = get_plot(Ticker, Request)
    
    return redirect(url_for('output'))

@app.route('/output', = ['POST'])
def output():
    x = result_plot
    script, div = components(x)
    return render_template('output.html', script=script, div=div)
    
if __name__ == '__main__':
    app.run(port=33507)
    
