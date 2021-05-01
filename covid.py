from bs4 import BeautifulSoup as soupp
from datetime import datetime , date
from urllib.request import Request, urlopen
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
import plotly.graph_objects as graph_objects
import plotly.offline as py
import plotly.express as px
import plotly.graph_objs as go
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
from pandas_profiling import ProfileReport

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
    df.drop([15, 16, 17, 18, 19, 20], inplace = True, axis = 1)

    column_labels = ["Country", "Total Cases", "New Cases", "Total Deaths", "New Deaths", "Total Recovered", "Active Cases", "Critical", "Total Cases/1M", "New Recovered", "Deaths/1M", "Total Test", "Test/1M", "Population", "Continent"]

    df.columns =  column_labels

    for label in df.columns:
        if label != 'Country' and label != "Continent":
         df[label] = pd.to_numeric(df[label])

    df["%Inc Cases"] = df["New Cases"]/df["Total Cases"]*100
    df["%Inc Deaths"] = df["New Deaths"]/df["Total Deaths"]*100
    df["%Inc Recovered"] = df["New Recovered"]/df["Total Recovered"]*100

    df.sort_values("Total Cases", axis = 0, ascending = False,
                 inplace = True, na_position ='first')

cases = df[["Total Recovered", "Active Cases", "Total Deaths"]].loc[0]
cases_df = pd.DataFrame(cases).reset_index()
cases_df.columns = ["Type", "Total"]

cases_df["Percentage"] = np.round(100*cases_df["Total"]/np.sum(cases_df["Total"]), 3)
cases_df["Virus Type"] = ["COVID-19" for i in range(len(cases_df))]  # |-_-|
fig_total = px.bar(cases_df, x = "Virus Type", y = "Percentage", color = "Type", hover_data = ["Total"])
# fig_total.show()
# print(fig_total)

perc = np.round(df[["%Inc Cases", "%Inc Deaths", "%Inc Recovered"]].loc[0], 2)

perc_df = pd.DataFrame(perc)
perc_df.columns = ["Percentage"]

fig_perc = px.bar(x = perc_df.index, y = perc_df["Percentage"], color = ["%Inc Cases", "%Inc Deaths", "%Inc Recovered"])

# fig_perc.show()
# print(perc_df)

# continent

continent_df = df.groupby("Continent").sum().drop("All")
continent_df = pd.DataFrame(continent_df).reset_index()
print(continent_df)

