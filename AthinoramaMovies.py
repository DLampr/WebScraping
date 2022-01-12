# Get All Athinorama Movies and their IMDB Rating and sort them by this rating

from bs4 import BeautifulSoup
import requests, json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re
from imdb import IMDb

driver = webdriver.Firefox()
driver.get('https://www.athinorama.gr/cinema/halls/abana-1001127')

selector = Select(driver.find_element_by_xpath('/html/body/main/section[2]/div[1]/div/form/fieldset/div/div[4]/div/select'))
options = selector.options

web_address = []

for i in options:
    value = i.get_attribute('value')
    web_address.append(value)
    
driver.close()

del web_address[0]
# web_address

greek_name = []
title = []
year = []
genre = []
imdb_rating = []
link = []

for i in web_address:
    url = f'https://www.athinorama.gr/cinema/movie/{i}'
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    all_a = soup.select('.external-links a')
    links = []

    for a in all_a:
        links.append(a['href'])
    
    try:
        ia = IMDb()
        movie = ia.get_movie(re.findall(r'\d+', links[0].split('/')[-2])[0])
        greek_name.append(soup.find('h1').text)
        year.append(soup.find('span', class_='year').text)
        title.append(movie['title'])
        genre.append(movie['genre'])
        imdb_rating.append(movie['rating'])
    except:
        pass
    
final = list(zip(greek_name, title, year, genre, imdb_rating))
df = pd.DataFrame(final, columns = ['greek_title', 'title', 'year', 'genres', 'imdb_rating'])
df.sort_values(by=['imdb_rating'], ascending = False)