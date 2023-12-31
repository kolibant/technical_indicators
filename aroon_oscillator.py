# Import dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
yf.pdr_override()

# input
symbol = "AAPL"
start = dt.date.today() - dt.timedelta(days=365 * 4)
end = dt.date.today()

# Read data
df = yf.download(symbol, start, end)

n = 25
high_max = lambda xs: np.argmax(xs[::-1])
low_min = lambda xs: np.argmin(xs[::-1])

df["Days since last High"] = (
    df["High"]
    .rolling(center=False, min_periods=0, window=n)
    .apply(func=high_max)
    .astype(int)
)

df["Days since last Low"] = (
    df["Low"]
    .rolling(center=False, min_periods=0, window=n)
    .apply(func=low_min)
    .astype(int)
)

df["Aroon_Up"] = ((25 - df["Days since last High"]) / 25) * 100
df["Aroon_Down"] = ((25 - df["Days since last Low"]) / 25) * 100

df["Aroon_Oscillator"] = df["Aroon_Up"] - df["Aroon_Down"]

df = df.drop(
    ["Days since last High", "Days since last Low", "Aroon_Up", "Aroon_Down"], axis=1
)

fig = plt.figure(figsize=(14, 7))
ax1 = plt.subplot(2, 1, 1)
ax1.plot(df["Adj Close"])
ax1.set_title("Stock " + symbol + " Closing Price")
ax1.set_ylabel("Price")
ax1.legend(loc="best")

ax2 = plt.subplot(2, 1, 2)
ax2.plot(df["Aroon_Oscillator"], label="Aroon Oscillator", color="g")
ax2.axhline(y=0, color="darkblue")
ax2.grid()
ax2.legend(loc="best")
ax2.set_ylabel("Aroon Oscillator")
ax2.set_xlabel("Date")
plt.show()
fig = plt.figure(figsize=(14, 7))
ax1 = plt.subplot(2, 1, 1)
ax1.plot(df["Adj Close"])
ax1.set_title("Stock " + symbol + " Closing Price")
ax1.set_ylabel("Price")
ax1.legend(loc="best")

df["Positive"] = df["Aroon_Oscillator"] > 0
ax2 = plt.subplot(2, 1, 2)
ax2.bar(
    df.index, df["Aroon_Oscillator"], color=df.Positive.map({True: "g", False: "r"})
)
ax2.axhline(y=0, color="red")
ax2.grid()
ax2.set_ylabel("Aroon Oscillator")
ax2.set_xlabel("Date")
plt.show()

# ## Candlestick with Aroon Oscillator

from matplotlib import dates as mdates

dfc = df.copy()
dfc["VolumePositive"] = dfc["Open"] < dfc["Adj Close"]
# dfc = dfc.dropna()
dfc = dfc.reset_index()
dfc["Date"] = mdates.date2num(dfc["Date"].tolist())
from mplfinance.original_flavor import candlestick_ohlc

fig = plt.figure(figsize=(14, 7))
ax1 = plt.subplot(2, 1, 1)
candlestick_ohlc(ax1, dfc.values, width=0.5, colorup="g", colordown="r", alpha=1.0)
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
ax1.grid(True, which="both")
ax1.minorticks_on()
ax1v = ax1.twinx()
colors = dfc.VolumePositive.map({True: "g", False: "r"})
ax1v.bar(dfc.Date, dfc["Volume"], color=colors, alpha=0.4)
ax1v.axes.yaxis.set_ticklabels([])
ax1v.set_ylim(0, 3 * df.Volume.max())
ax1.set_title("Stock " + symbol + " Closing Price")
ax1.set_ylabel("Price")

df["Positive"] = df["Aroon_Oscillator"] > 0
ax2 = plt.subplot(2, 1, 2)
ax2.bar(
    df.index, df["Aroon_Oscillator"], color=df.Positive.map({True: "g", False: "r"})
)
ax2.axhline(y=0, color="red")
ax2.grid()
ax2.set_ylabel("Aroon Oscillator")
ax2.set_xlabel("Date")
plt.show()