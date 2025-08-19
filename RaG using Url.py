# Databricks notebook source
import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup=BeautifulSoup(response.text,"html.parser")
        text_data=" ".join([p.get_text() for p in soup.find_all('p')])
        return text_data
    else:
        return None
    
url="https://www.databricks.com/"
text_content=scrape_website(url)
print(text_content)