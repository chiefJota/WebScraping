from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import Counter
import csv

summary = []
directors = []
cast_list = []

#----------------------------------------------------------------------------#
# Scrapes the IMDB's site
source = requests.get('http://www.imdb.com/chart/top').text
soup = BeautifulSoup(source, 'html.parser')
movie_scrap_lines = soup.find_all('td', attrs={'class': 'titleColumn'})
movie_ratings = soup.find_all('td', attrs={"class" : 'ratingColumn imdbRating'})
 #get the poster column for the movies
movie_posters = soup.find_all('td', attrs={'class': 'posterColumn'})


#gets rank, title, date, and link
def get_movie_info(movie_info):
    return (movie_info.contents[0][7:-8],
            movie_info.contents[1].text,
            movie_info.find('span').text[1:-1], movie_info.contents[1].get('href'))

#gets rating
def get_movie_rating(movie_ratings):
    return movie_ratings.contents[1].text

#get image for each movie
def get_movie_poster(movie_poster,soup):
   #get contents
    posters = soup.select('img[src^="https://m.media-amazon"]')
    for poster in posters:
        poster_link = poster['src']
        poster_alt = poster['alt']
        print()

    
  
get_movie_poster(movie_posters, soup)


#builds movie info and moving ratings for dataframes
movie_infos = [get_movie_info(movie_scrap_line) for movie_scrap_line in movie_scrap_lines] 
movie_rates =[get_movie_rating(movie_rating) for movie_rating in movie_ratings]

# Dump the result into a csv file
df = pd.DataFrame(movie_infos, columns=['number', 'title', 'year', 'link'])
df2 = pd.DataFrame(movie_rates, columns=['rating'])
df.to_csv('movielist.csv', index=False, encoding='utf-8')
df2.to_csv('movierating.csv', index=False, encoding='utf-8')

#----------------------------------------------------------------------------#
#now get the director, description, and cast

#gets the movie summary
def get_movie_summary(movie_summary):
    global summary
    the_summary = movie_summary.text
    theStory = the_summary.strip()
    summary.append(theStory)
    return summary

#gets the director and main cast members
def get_movie_details(movie_details):
    global directors
    director = movie_details.contents[3].text
    directors.append(director)
    return directors

def get_movie_cast(movie_details, broth):
    global cast_list
    actors_movie = []
    results = broth.select('div.credit_summary_item > h4:contains("Stars:")~a[href^="/name/"]')

    for result in results:
        actors_movie.append(result.text)
    cast_list.append(actors_movie)
   # print(cast_list)
    return cast_list


    

# Go through csv file and get the links for each movie
with open('movielist.csv') as csvfile:
    links = []
    readCSV = csv.reader(csvfile, delimiter=',')
    # put the links in a list 
    for row in readCSV:
        link = row[3]
        links.append(link)

def collect_data():
    #create string to mutate
    http = "https://www.imdb.com"
    address = " "
   #skip the column name
    for link in links[1:]:
        #address we want is link
        address = http + link
        #get the source
        source = requests.get(address).text
        broth = BeautifulSoup(source, 'html.parser')

        movie_summary = broth.find('div', attrs={'class' : 'summary_text'})
        movie_details = broth.find('div', attrs={'class' : 'credit_summary_item'})
        movie_cast = broth.find('h4', attrs={'class' : 'inline'})


        #builds movie info and moving ratings for dataframes
        movie_stuff = get_movie_details(movie_details) 
        summaries = get_movie_summary(movie_summary) 
        movie_cast = get_movie_cast(movie_details, broth) 
    

        d_f = pd.DataFrame(movie_stuff, columns=['director'])
        d_f2 = pd.DataFrame(summaries, columns=['summary'])
        d_f3 = pd.DataFrame(movie_cast, columns=['cast', 'cast2', 'cast3'])

    d_f.to_csv('movieDetails.csv', index=False, encoding='utf-8')
    d_f2.to_csv("movieSummaries.csv", index=False, encoding='utf-8')
    d_f3.to_csv("movieCast.csv", index=False, encoding='utf-8')
    
    
#----------------------------------------------------------------------------#

def main(): 

    collect_data()

if __name__ == "__main__":
    main()

