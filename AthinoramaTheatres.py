"""Get all the Theatres in Athens from Athinorama Website using Selenium & BeautifulSoup"""

from bs4 import BeautifulSoup
import requests, json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()
driver.get('https://www.athinorama.gr/theatre/halls/idruma_%C2%ABmixalis_kakogiannis%C2%BB-2000798')

selector = Select(driver.find_element_by_id('roomSelect'))
options = selector.options

name=[]

for index in range(0, len(options)-1):
    name.append(options[index].text)

web_address = []

for i in options:
    value = i.get_attribute('value')
    web_address.append(value)

driver.close()

del name[0]
del web_address[0]

addresses = []
name_new = []
for i in web_address:
    url = f'https://www.athinorama.gr/theatre/halls/{i}'
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    try:
        html = soup.find('div', class_='infos-item')
        a_tag = html.a
        link = a_tag.text
        name_new.append(soup.title.text.split(" - ")[0].strip())
        addresses.append(link)
    except:
        name_new.append(soup.title.text.split(" - ")[0].strip())
        addresses.append('None')
    
final = list(zip(name, name_new, addresses, web_address))

df = pd.DataFrame(final, columns = ["name_", "name", "address", "web_address"])
# df.to_csv("C:/___your_path_here___/Theatres.csv")