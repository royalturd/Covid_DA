from bs4 import BeautifulSoup as soupp
from datetime import datetime , date
from urllib.request import Request, urlopen
import pandas as pd
import numpy as np

today = datetime.now()

yesterday_str = '%s %d,%d' %(date.today().strftime("%b") , today.day-1 , today.year)
yesterday_str

##web scraping

url = "https://www.worldometers.info/coronavirus/?fbclid=IwAR35ZFiRZJ8tyBCwazX2N-k7yJjZOLDQiZSA_MsJAfdK74s8f2a_Dgx4iVk#countries"
req = Request(url , headers={'User-Agent':"Mozilla/5.0"})

webpage = urlopen(req)
page_soupp = soupp(webpage, "html.parser")
table: list = page_soupp.findAll("table",{"id": "main_table_countries_yesterday"})

containers = table[0].findAll("tr",{"style":""})
title = containers[0]

del containers[0]

all_data = []
clean = True
for country in containers:
    country_data = []
    country_container = country.findAll("td")

    if country_container[0].text == "China":
        continue
    for i in range (1, len(country_container)):
        final_feature = country_container[i].text
        if clean:
            if i != 1 and i != len(country_container)-1:
                final_feature = final_feature.replace(",","")   #to replace comma
                if final_feature.find("+") != -1:
                    final_feature = final_feature.replace("+","") #to replace +
                    final_feature = float(final_feature)
                elif final_feature.find("-") != -1 :
                    final_feature = final_feature.replace("-","") #to replace -
                    final_feature = float(final_feature)*-1
        if  final_feature == 'N\A':
            final_feature = 0
        elif final_feature == " " or final_feature == "":
             final_feature = -1
        country_data.append(final_feature)
    all_data.append(country_data)


    df = pd.DataFrame(all_data)
    print(df.head())
        
            

