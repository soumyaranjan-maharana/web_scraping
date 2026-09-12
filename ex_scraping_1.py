from bs4 import BeautifulSoup
import requests
import pandas as pd


response = requests.get("https://quotes.toscrape.com/page/1/")
soup = BeautifulSoup(response.text, "html.parser")


page1 = soup.find_all("div", class_ = "col-md-8")[1]
quotes = page1.find_all("span", class_ = "text")
author = page1.find_all("small", class_ = "author")

# for q in quotes:
#     print(q.text)
# for a in author:
#     print(a.text)

df = pd.DataFrame(columns=["Quotes", "Author"],)

for i, q in enumerate(quotes):
    df.loc[i, "Quotes"] = q.text
for i, a in enumerate(author):
    df.loc[i, "Author"] = a.text

df.to_csv(r"C:\Users\Lenovo\OneDrive\Documents\dataframe files\quates.csv", index=False, encoding="utf-8-sig")