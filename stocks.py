import streamlit as st
import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si
import yfinance as yf
import matplotlib.pyplot as plt
st.title('Stocks')


@st.cache
def read():
    dfx = pd.read_excel("/root/stocks/symbolsStock.xlsx")
    return dfx
df = read()
def getStockArray(stocksSelected1, stocksSelected2,dic):
    selectedALL = stocksSelected1

    for i in stocksSelected2:
        for j in dic:
            if dic[j] == i:
                selectedALL.append(j)
    selectedALL = list(set(selectedALL))
    return selectedALL

listofAllstocks = df["Symbol"].tolist()
listofAllNames = df["Name"].tolist()
stocksSelected1 = st.multiselect("Pick Stock(Symbol)", listofAllstocks)
stocksSelected2 = st.multiselect("Pick Stock(Name)", listofAllNames)
dic = dict(zip(listofAllstocks, listofAllNames))
st.sidebar.title("List of Stocks")
show = st.sidebar.button("Show Stocks")
if show:
    for i in dic :
        st.sidebar.markdown(str(i)+str(dic[i]))

startdate = st.text_input("Start date for displaying stocks", "2015-5-2")
enddate = st.text_input("Ending date for displaying stocks", "2016-2-4")
duration = st.selectbox("Which Duration do you want ", ["1d", "1mo", "1y"])

showStock = st.button("Show")
if showStock:
    selected = getStockArray(stocksSelected1, stocksSelected2, dic)
    for i in selected:

        try:
            st.write(i, si.get_live_price(i))
            tickerData = yf.Ticker(i)
            tickerDf = tickerData.history(period=duration, start=startdate, end=enddate)
            closedf = tickerDf["Close"]
            st.write(tickerDf)
            lines = tickerDf.plot.line()
            st.line_chart(closedf)

        except:
            st.write("Error", i)
st.title('---------')




