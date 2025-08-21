import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
#no idea the errors above it runs so do not care

#to calculate high rate and investment rate from price per 100
# def high_rate(priceperhundred,weeks):
#     # priceperhundred = pd.to_numeric(priceperhundred, errors='coerce')
#     weeks = weeks.str.extract(r'(\d+)').astype('float').squeeze()
#     rate_received = ((((100-priceperhundred)*365)/(1000*weeks*7))*100)
#     return rate_received    

def high_rate(pph,weeks):
    # weeks = weeks.str.extract(r'(\d)').astype('int').squeeze()
    weeks = (weeks.str.extract(r'(\d+)').astype(int)).squeeze()
    # rate_received = ((100-pph)/(weeks*7))*364
    rate_received = ((((100-pph)*360)/(1000*weeks*7))*100)
    # rate_received = weeks
    return rate_received    

def investment_rate(priceperhundred,wks):
    wks = (wks.str.extract(r'(\d+)').astype(int)).squeeze()
    actual_percent_received = (((100-priceperhundred)/priceperhundred)*365)/(wks*7)
    return actual_percent_received


# I need to make 2 data sets that each are the securities and then from there i 
# concatonate both and drop data that have the same cusip
# then I will remove anything in column 2 that does not have bill
#i am going to remove maturity date 
#then i am going to add 2 columns which are high rate and investment rate which can be used from these programs 
#then from there i can do graphs and analyze the data 

securities_one = pd.read_csv(r"C:\Users\noahf\Downloads\Sexcurities (6).csv")
securities_two = pd.read_csv(r"C:\Users\noahf\Downloads\Securities (7).csv")

data = pd.concat([securities_one, securities_two], ignore_index=True)


data = data[data['Security Term'].str.contains('Week') & (data['Security Type'] == 'Bill')]

data.drop('Maturity Date', axis=1, inplace=True)

data = data.dropna(thresh=6)
data['Price per $100'] = data['Price per $100'].astype(float)

data['High Rate'] = high_rate(data['Price per $100'], data['Security Term'])*10

data['Investment Rate'] = investment_rate(data['Price per $100'],data['Security Term'])*100

# treasuryData = pd.read_csv('treasuryScraperAnalysis.csv')

# dataCombined = pd.concat([treasuryData, data], ignore_index=True)

dataCombined = data
dataCombined['Issue Date'] = pd.to_datetime(data['Issue Date'])
dataCombined.sort_values(by='Issue Date', inplace=True, ascending = False)

dataCombined = dataCombined.dropna(thresh=8)

dfFinal = dataCombined.drop_duplicates(subset=['CUSIP'], keep='first')

# dfFinal['High Rate'].plot(kind='hist', bins=30, title='Distribution of High Rates')
# plt.show()

# dfFinal['Investment Rate'].plot(kind='hist',bins=30, title='Box Plot of Investment Rates')
# plt.show()
dfFinal.to_csv('treasuryScraperAnalysis.csv',index=False)

