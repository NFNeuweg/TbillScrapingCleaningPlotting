#imma just add this in here because it definitely will confuse me later on so the high rate is the percent of the 100 you have to buy it in 
#the investment rate is the percentage you get back on what you actually spend 
#for example you register to buy a 100 dollar bill at like 5% for 1 year. you dont actually spend 100 dollars
#you spend like 95 and get paid 100 the high rate is the 5% you would get the investment rate is 5.26% bc you only spent 95$


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


#no idea the errors above it runs so do not care

#this is the path to chrome driver exe in the python prac folder
#no idea what service does but need that
#driver is the webdriver so it is calling it 

#chromedriver_path = "C:\PythonPrac\chromedriver-win64\chromedriver.exe"
#service = Service(chromedriver_path)
#driver = webdriver.Chrome(service=service)

#just installs the right manager for chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
#url to site
url = "https://treasurydirect.gov/auctions/announcements-data-results/"
driver.get(url) #gets the url

#wait for the page to load
driver.implicitly_wait(50)

#gets the entire html part of it 
html = driver.page_source

#this just uses beautiful soups way to parse html files 
soup = BeautifulSoup(html, 'html.parser')


#quits selenium 
driver.quit()

#now we start to parse the data

#we gon start by finding the div it is in
div = soup.find('div',{'id':'myTabContent'})
#check if div was found
if div:
    print('da div found')
    #now we go to the next div
    div2 = soup.find('div',{'id':'tabs-1'})
    #check if div was found
    if div2:
        print('the second div found')
        table = div2.find('table',{'id':"institTableBills"})
        #check if table was found
        if table:
            print('finafckingly found the table')
            #now we find the rows and extract it 
            rows = table.find_all('tr')

            #creating a data set
            data = []

            #we go to each column and i am taking out the cusip the term issue date high rate and investment rate
            for row in rows[1:]:
                cells = row.find_all('td')
                
                if len(cells) >= 6:
                    security_term = cells[0].text.strip()
                    #this is just to confirmt that it is just taking data for weeks
                    if 'Week' in security_term:
                        cusip = cells[1].text.strip()
                        issue_date = cells[2].text.strip()
                        high_rate = cells[4].text.strip()
                        investment_rate = cells[5].text.strip()

                    
                    #now we add this data we took out to a list
                    data.append([security_term,cusip,issue_date,high_rate,investment_rate])
        else:
            print('table not found')
    else:
        print('div 2 not found')
else:
    print('first div not found')    


#now we create a pandas dataframe to hold the data

df = pd.DataFrame(data, columns=('Security Term Weeks','CUSIP','Issue Date','High Rate','Investment Rate')) 
#this writes it out to a csv file


df['Issue Date'] = pd.to_datetime(df['Issue Date'],format='%m/%d/%Y')
#now what i have to do is get the csv file it will export to then make it a data frame and drop duplicate cusips 
try:
    treasuryData = pd.read_csv('treasury_auction_results.csv')
except FileNotFoundError:
    treasuryData = pd.DataFrame(columns=['Security Term Weeks', 'CUSIP', 'Issue Date', 'High Rate', 'Investment Rate'])

#concatonates what is there
dataCombined = pd.concat([treasuryData, df], ignore_index=True)
#organizes by date
dataCombined['Issue Date'] = pd.to_datetime(dataCombined['Issue Date'],errors='coerce')
dataCombined.sort_values(by='Issue Date', inplace=True, ascending = False)
#will drop duplicates that have the same cusip 
dfFinal = dataCombined.drop_duplicates(subset=['CUSIP'], keep='first')

# export it back to treeasury auctionresults
dfFinal.to_csv('treasury_auction_results.csv', index=False)

