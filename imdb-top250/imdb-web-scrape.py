from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import csv


# Scrapes the IMDB's site
source = requests.get('http://www.imdb.com/chart/top').text
soup = BeautifulSoup(source, 'html.parser')
movie_scrap_lines = soup.find_all('td', attrs={'class': 'titleColumn'})
movie_ratings = soup.find_all('td', attrs={"class" : 'ratingColumn imdbRating'})


#gets rank, title, date, and link
def get_movie_info(movie_info):
    return (movie_info.contents[0][7:-8],
            movie_info.contents[1].text,
            movie_info.find('span').text[1:-1], movie_info.contents[1].get('href'))

#gets rating
def get_movie_rating(movie_ratings):
    return movie_ratings.contents[1].text

movie_infos = [get_movie_info(movie_scrap_line) for movie_scrap_line in movie_scrap_lines] 
movie_rates =[get_movie_rating(movie_rating) for movie_rating in movie_ratings]

# Dump the result into a csv file
df = pd.DataFrame(movie_infos, columns=['number', 'title', 'year', 'link'])
df2 = pd.DataFrame(movie_rates, columns=['rating'])
df.to_csv('movielist.csv', index=False, encoding='utf-8')
df2.to_csv('movierating.csv', index=False, encoding='utf-8')

a = pd.read_csv("movielist.csv")
b = pd.read_csv("movierating.csv")
merged = a.merge(b,left_on='link')
merged.to_csv('test.csv', index=False, encoding='utf-8')