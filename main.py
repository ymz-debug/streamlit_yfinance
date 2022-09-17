import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt

# SB
days = 20
tickers = {
    'SB': '9984.T',
    'NTT': '9432.T',
    'KDDI': '9433.T',
    'Yahoo': '4689.T',
    '楽天': '4755.T'
}

def get_data(days, tickers):
    df = pd.DataFrame()

    for company in tickers.keys():
        
        tkr = yf.Ticker(tickers[company])

        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%y/%m/%d')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

dt = get_data(days, tickers)


companies = ['SB', 'NTT']
data = dt.loc[companies]

data = data.T.reset_index()

data = pd.melt(data, id_vars=['Date']).rename(columns={'value': '終値'})

data

ymin, ymax = 3000, 6000

chart = (
    alt.Chart(data)
    .mark_line(opacity=0.8, clip=True)
    .encode(
        x="Date",
        y=alt.Y("終値:Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
        color="Name:N"
    )
)

chart


# def Column_Mod(hist, C_name):
#     hist = hist[['Close']]
#     hist.columns = [f'{C_name}']
#     hist.index = hist.index.strftime('%y/%m/%d')
#     hist = hist.T
#     hist.index.name = 'Name'
#     return hist



# # yahoo
# Yahoo = yf.Ticker('4689.T')
# Yhist = Yahoo.history(period=f'{days}d')
# Yhist = Column_Mod(Yhist, 'Yahoo')

# print(Yhist)
