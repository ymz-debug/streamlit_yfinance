import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('通信事業者株価可視化')

st.sidebar.write("""
# 事業者
下のオプションから表示日数を指定
"""
)

st.sidebar.write("""
表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
### 過去 **{days}日間** の株価
"""
)

@st.cache
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

try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
    '範囲を指定してください',
    0.0, 6500.0, (0.0, 6500.0)
    )

    tickers = {
        'SB': '9984.T',
        'NTT': '9432.T',
        'KDDI': '9433.T',
        'Yahoo': '4689.T',
        '楽天': '4755.T'
    }

    dt = get_data(days, tickers)

    companies = st.multiselect(
        '事象社を選択',
        list(dt.index),
        ['SB','NTT','KDDI', 'Yahoo', '楽天']
    )

    if not companies:
        st.error('事業者を選んでください')
    else:
        data = dt.loc[companies]
        st.write('### 終値（円）', data.sort_index())
        data = data.T.reset_index()

        data = pd.melt(data, id_vars=['Date']).rename(columns={'value': '終値'})
        
        chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x="Date",
            y=alt.Y("終値:Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
            color="Name:N"
        )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "エラーが起きているようです"
    )

