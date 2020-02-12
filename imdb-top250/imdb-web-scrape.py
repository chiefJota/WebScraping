from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import Counter
import csv

#----------------------------------------------------------------------------#
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

#builds movie info and moving ratings for dataframes
movie_infos = [get_movie_info(movie_scrap_line) for movie_scrap_line in movie_scrap_lines] 
movie_rates =[get_movie_rating(movie_rating) for movie_rating in movie_ratings]

# Dump the result into a csv file
df = pd.DataFrame(movie_infos, columns=['number', 'title', 'year', 'link'])
df2 = pd.DataFrame(movie_rates, columns=['rating'])
df.to_csv('movielist.csv', index=False, encoding='utf-8')
df2.to_csv('movierating.csv', index=False, encoding='utf-8')
#----------------------------------------------------------------------------#

#now get the director, description, cast, and image for each movie
source = requests.get("https://www.imdb.com/title/tt0111161/").text
stew = BeautifulSoup(source, 'html.parser')
movie_summary = stew.find('div', attrs={'class' : 'summary_text'})
movie_details = stew.find('div', attrs={'class' : 'credit_summary_item'})
#movie_cast = stew.find('h4', attrs={'class' : 'inline'}, string="Stars:")

#gets the movie summary
def get_movie_summary(movie_summary):
    return movie_summary.text
summary = get_movie_summary(movie_summary)

#gets the director and main cast members
def get_movie_details(movie_details):
    director = movie_details.contents[3].text
    print(director)

def get_movie_cast(movie_cast):
    cast_list = []
    cast1 = movie_cast.find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next()
    cast2 = movie_cast.find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next()
    cast3 = movie_cast.find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next()
    star1 = cast1.text
    star2 = cast2.text
    star3 = cast3.text
    cast_list.append(star1)
    cast_list.append(star2)
    cast_list.append(star3)
    for cast in cast_list:
        print(cast)


get_movie_details(movie_details)
get_movie_cast(movie_details)


#TODO: 
# Go through csv file and get the links for each movie
# put the links in a list and iterate over the list until done
# get the description, director, and cast for each movie
#get the photo of the movie
