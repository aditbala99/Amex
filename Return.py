import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
amex = pd.read_csv("AXP_weekly_return_detailed.csv")
amex = amex[amex["Year"] == 2022].reset_index(drop=True)
df_2022 = amex[amex['Year']==2022]
print(df_2022)

#df_2022['Labels'] = df_2022.apply(lambda row: 'Green' if row.volatility > 1.70 else 'Red')
df_volatility=df_2022['volatility']
print(df_volatility)
type(df_volatility)
df_volatility.astype(int)

df_2022['Labels']=['Green' if i > 1.70 else 'Red' for i in df_volatility]
print(df_2022)



amount_cash = 100
stocks_bought = 0
c = 1
invested_first_time = False
invested = False



for i in range(0, len(df_2022)):
    a = df_2022.loc[i,'Labels']
    if invested_first_time == False:
        if a == "Green":
            df1 = df_2022[df_2022["Week_Number"] == c]
            df1=df1.reset_index()
            open_value = df1.loc[0,'Open']
            stocks_bought = round(amount_cash / open_value, 2)
            amount_cash = 0
            invested_first_time = True
            invested = True
            c += 1
        elif a == "Red":
            c += 1
    else:
        if invested == True and a == "Green":
            c += 1
        elif invested == True and a == "Red":
            df1 = df_2022[df_2022["Week_Number"] == c - 1]
            adj_close_value = df1.iloc[-1][r'Adj Close']

            amount_cash = stocks_bought * adj_close_value
            stocks_bought = 0
            invested = False
            c += 1
        elif invested == False and a == "Green":
            df1 = df_2022[df_2022["Week_Number"] == c]
            open_value = df1.loc[0, 'Open']
            stocks_bought = round(amount_cash/ open_value, 2)
            amount_cash = 0
            invested = True
            c += 1
        elif invested == False and a == "red":
            c += 1
    print(a, c, stocks_bought, amount_cash)


if stocks_bought != 0:
    df1 = df_2022[df_2022["Week_Number"] == 52]
    adj_close_value = df1.loc[-1 , r'Adj Close']
    amount_cash = adj_close_value * stocks_bought
    stocks_bought = 0
print(amount_cash)


#Buy and Hold
df_2022 = df_2022.sort_values(by="Week_Number")

# Invest $100 on the first trading day at the opening price
investment = 100
shares = investment / df_2022.iloc[0]["mean_return"]

# Sell at the last trading day at the adjusted closing price
pnl = shares * df_2022.iloc[-1]["mean_return"] - investment

print("Profit/Loss for Buy-and-Hold Strategy: ${:.2f}".format(pnl))
