import pandas as pd
import matplotlib as mpl
import numpy as np
import plotly.express as px

df = pd.read_csv("treasuryScraperAnalysis.csv")
df['Issue Date'] = pd.to_datetime(df['Issue Date'])
fig = px.line(df, x='Issue Date', y='Investment Rate', color='Security Term',title='Investment Rate by Security Term Over Time')
fig.show()


dOther = pd.read_csv('treasury_auction_results.csv')
#need to convert to real time otherwise plotly get weird and I have to change the % into numbers
dOther['Issue Date'] = pd.to_datetime(dOther['Issue Date'])
dOther['Investment Rate'] = dOther['Investment Rate'].astype(str).str.replace('%','',regex = False).astype(float)/100.0
figure = px.line(dOther, x='Issue Date', y = 'Investment Rate',color='Security Term Weeks', title='Investment rate On Going over time')
figure.show()

# print(dOther.head())
# print(dOther.describe())

#how much expected



TERM_DAYS = {"4-Week":28,"8-Week":56,"13-Week":91,"17-Week":119,"26-Week":182,"52-Week":364}

def last5_avg_rate(df, term):
    sub = df[df["Security Term Weeks"] == term].sort_values("Issue Date").tail(5)
    return float(sub["Investment Rate"].mean())

def t_bill_from_cash(cash, rate, days):
    raw_face = cash * (1 + rate * days / 365.0)
    face = max(100, round(raw_face/100)*100)        # $100 increments
    price = face / (1 + rate * days / 365.0)        # what you actually pay
    profit = face - price
    return price, face, profit


while True:
    term = input('Which term(4,8,13,17,26,52)')
    matches = [k for k in TERM_DAYS if term in k]
    if len(matches) == 1:
        term = matches[0]
        break
    elif len(matches) > 1:
        print(f"Try again: {matches}")
    else:
        print("Try again")
cash = float(input('How much do you want to invest round to lowest 100   '))
rate = last5_avg_rate(dOther, term)
days = TERM_DAYS[term]
price, face, profit = t_bill_from_cash(cash, rate, days)
print(f"{term}: pay ${price:.2f} today → receive ${face:.0f} at maturity (profit ${profit:.2f}; annualized {profit/price*365/days*100:.2f}%).")
print('This is based on the past 5 Tbill rates')