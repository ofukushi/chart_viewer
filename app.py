
# # weekly_kargin_interest/app.py

# import os
# import json
# import datetime as dt
# import logging
# from flask import Flask, render_template, request
# import psycopg2
# import requests
# import pandas as pd
# import plotly.graph_objs as go
# from urllib.parse import urlparse
# from dotenv import load_dotenv
# load_dotenv(dotenv_path="/mnt/c/Users/osamu/OneDrive/onedrive_python_source/envs/.env.chart_viwer")
# from utils.auth import get_id_token
# from utils.fetch import (
#     fetch_weekly_margin_interest,
#     fetch_company_name,
#     fetch_short_selling_positions,
#     fetch_daily_quotes
# )


# # Setup logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# app = Flask(__name__)

# def plot_candlestick(df_prices):
#     return go.Candlestick(
#         x=df_prices['Date'],
#         open=df_prices['AdjustmentOpen'],
#         high=df_prices['AdjustmentHigh'],
#         low=df_prices['AdjustmentLow'],
#         close=df_prices['AdjustmentClose'],
#         name='Stock Price'
#     )

# def plot_long_margin(df_margin):
#     return go.Bar(
#         x=df_margin['Date'],
#         y=df_margin['ScaledLongMargin'],
#         name='Long Margin Volume',
#         yaxis='y2',
#         marker_color='blue',
#         opacity=0.7
#     )

# def plot_short_margin(df_margin):
#     return go.Bar(
#         x=df_margin['Date'],
#         y=df_margin['ScaledShortMargin'],
#         name='Short Margin Volume',
#         yaxis='y2',
#         marker_color='red',
#         opacity=0.7
#     )

# def plot_short_selling_positions(df_shorts):
#     return go.Scatter(
#         x=df_shorts["CalculatedDate"],
#         y=df_shorts["ScaledShortShares"],
#         mode='lines+markers',
#         name="Outstanding Short Positions",
#         yaxis="y2",
#         line=dict(color='darkorange', width=2, dash='dot')
#     )

# def create_combined_chart(df_prices, df_margin, df_shorts, company_name):
#     df_prices['Date'] = pd.to_datetime(df_prices['Date'])
#     df_margin['Date'] = pd.to_datetime(df_margin['Date'])
#     df_shorts['CalculatedDate'] = pd.to_datetime(df_shorts['CalculatedDate'])

#     df_margin['ScaledShortMargin'] = df_margin['ShortMarginTradeVolume'] / 1000
#     df_margin['ScaledLongMargin'] = df_margin['LongMarginTradeVolume'] / 1000

#     fig = go.Figure(data=[
#         plot_candlestick(df_prices),
#         plot_long_margin(df_margin),
#         plot_short_margin(df_margin),
#         plot_short_selling_positions(df_shorts)
#     ])

#     fig.update_layout(
#         title=f'Stock Price & Margin Interest for {company_name}' if company_name else 'Stock Price & Margin Interest',
#         xaxis={'title': 'Date'},
#         yaxis={'title': 'Price'},
#         yaxis2={
#             'title': 'Margin / Short Vol. (×1,000)',
#             'overlaying': 'y',
#             'side': 'right'
#         },
#         height=750,
#         barmode='overlay'
#     )

#     return fig.to_html(full_html=False)

# # Flask Views
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     chart_html = ""
#     company_name = ""
#     error_message = ""

#     if request.method == 'POST':
#         raw_code = request.form['code'].strip()
#         code = raw_code if len(raw_code) == 5 else raw_code + "0"

#         id_token = get_id_token()

#         df_margin = fetch_weekly_margin_interest(code, id_token)
#         df_prices = fetch_daily_quotes(code, id_token)
#         df_shorts = fetch_short_selling_positions(code, id_token)
#         company_name = fetch_company_name(code, id_token)

#         if df_prices.empty or df_margin.empty:
#             error_message = f"データが見つかりませんでした: 証券コード {raw_code} を確認してください。"
#         else:
#             chart_html = create_combined_chart(df_prices, df_margin, df_shorts, company_name or raw_code)

#     return render_template('index.html', chart=chart_html, company_name=company_name, error_message=error_message)


# if __name__ == '__main__':
#     app.run(debug=True)

# weekly_kargin_interest/app.py

import os
import json
import datetime as dt
import logging
from flask import Flask, render_template, request
import psycopg2
import requests
import pandas as pd
import plotly.graph_objs as go
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv(dotenv_path="/mnt/c/Users/osamu/OneDrive/onedrive_python_source/envs/.env.chart_viwer")
from utils.auth import get_id_token
from utils.fetch import (
    fetch_weekly_margin_interest,
    fetch_company_name,
    fetch_short_selling_positions,
    fetch_daily_quotes
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

app = Flask(__name__)

def plot_candlestick(df_prices):
    return go.Candlestick(
        x=df_prices['Date'],
        open=df_prices['AdjustmentOpen'],
        high=df_prices['AdjustmentHigh'],
        low=df_prices['AdjustmentLow'],
        close=df_prices['AdjustmentClose'],
        name='Stock Price'
    )

def plot_long_margin(df_margin):
    return go.Bar(
        x=df_margin['Date'],
        y=df_margin['ScaledLongMargin'],
        name='Long Margin Volume',
        yaxis='y2',
        marker_color='blue',
        opacity=0.7
    )

def plot_short_margin(df_margin):
    return go.Bar(
        x=df_margin['Date'],
        y=df_margin['ScaledShortMargin'],
        name='Short Margin Volume',
        yaxis='y2',
        marker_color='red',
        opacity=0.7
    )

def plot_short_selling_positions(df_shorts):
    if df_shorts is None or df_shorts.empty or 'ScaledShortShares' not in df_shorts.columns:
        logging.warning("No valid short selling data to plot.")
        return []
    return go.Scatter(
        x=df_shorts["CalculatedDate"],
        y=df_shorts["ScaledShortShares"],
        mode='lines+markers',
        name="Outstanding Short Positions",
        yaxis="y2",
        line=dict(color='darkorange', width=2, dash='dot')
    )

def create_combined_chart(df_prices, df_margin, df_shorts, company_name):
    df_prices['Date'] = pd.to_datetime(df_prices['Date'])
    df_margin['Date'] = pd.to_datetime(df_margin['Date'])

    df_margin['ScaledShortMargin'] = df_margin['ShortMarginTradeVolume'] / 1000
    df_margin['ScaledLongMargin'] = df_margin['LongMarginTradeVolume'] / 1000

    if df_shorts is not None and not df_shorts.empty and 'CalculatedDate' in df_shorts.columns:
        df_shorts['CalculatedDate'] = pd.to_datetime(df_shorts['CalculatedDate'])

    traces = [
        plot_candlestick(df_prices),
        plot_long_margin(df_margin),
        plot_short_margin(df_margin)
    ]

    short_plot = plot_short_selling_positions(df_shorts)
    if short_plot:
        traces.append(short_plot)

    fig = go.Figure(data=traces)

    fig.update_layout(
        title=f'Stock Price & Margin Interest for {company_name}' if company_name else 'Stock Price & Margin Interest',
        xaxis={'title': 'Date'},
        yaxis={'title': 'Price'},
        yaxis2={
            'title': 'Margin / Short Vol. (×1,000)',
            'overlaying': 'y',
            'side': 'right'
        },
        height=750,
        width=None,  # Let HTML/CSS handle width
        autosize=True, 
        barmode='overlay'
    )

    return fig.to_html(full_html=False)

# Flask Views
@app.route('/', methods=['GET', 'POST'])
def index():
    chart_html = ""
    company_name = ""
    error_message = ""

    if request.method == 'POST':
        raw_code = request.form['code'].strip()
        code = raw_code if len(raw_code) == 5 else raw_code + "0"

        id_token = get_id_token()

        df_margin = fetch_weekly_margin_interest(code, id_token)
        df_prices = fetch_daily_quotes(code, id_token)
        df_shorts = fetch_short_selling_positions(code, id_token)
        company_name = fetch_company_name(code, id_token)

        if df_prices.empty or df_margin.empty:
            error_message = f"データが見つかりませんでした: 証券コード {raw_code} を確認してください。"
        else:
            chart_html = create_combined_chart(df_prices, df_margin, df_shorts, company_name or raw_code)

    return render_template('index.html', chart=chart_html, company_name=company_name, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
