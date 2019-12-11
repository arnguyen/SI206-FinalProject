import spotifyCollection
import weather
import sqlite3
import os
import sys
import requests
from collections import defaultdict
import statistics

#### Deals with user input for running data collection ####

def dataCollection():   
    usr_input = input("Do you want to collect data? [y/n]")
    if usr_input.lower() == 'y':  
        dataCollectionHandler()
    elif usr_input.lower() == 'n':
        return
    else:
        print("Invalid input. Please try again.")
        return dataCollection()

def dataCollectionHandler():
    usr_input = input("Would you like to collect track data, weather data, or both? [t/w/b]")
    if usr_input.lower() == 't':
        spotifyCollection.main()
    elif usr_input.lower() == 'w':
        weather.main()
    elif usr_input.lower() == 'b':
        spotifyCollection.main()
        weather.main()
    else:
        print("Invalid input. Please try again.")
        return dataCollectionHandler()

#############################


#### Connect to database ####

def databaseConnection(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

##############################


#### Calculations for popularity and genre ####

def popularityGenre(cur, conn):
    joined_data = []
    for row in cur.execute('SELECT Tracks.Popularity, Genres.Title FROM Tracks INNER JOIN Genres ON Tracks.genre_id=Genres.genre_id'):
        joined_data.append((row[0], row[1]))
    return joined_data

def avgGenrePopularity(data):
    genredict = defaultdict(list)
    for item in data:
        genredict[item[1]].append(item[0])
    genredict = dict(genredict)

    pop_means = []
    for pop in genredict.values():
        popavg = statistics.mean(pop)
        pop_means.append(popavg)

    genres = []
    for genre in genredict:
        genres.append(genre)

    genremeans = {}
    for i in range(len(genres)):
        genremeans[genres[i]] = pop_means[i]

    return genremeans

##############################


#### Calculations for City and Temperature ####

def cityTemps(cur, conn):
    joined_data = []
    for row in cur.execute('SELECT Weather_Data.Temp_Min, Weather_Data.Temp_Max, Cities.City FROM Weather_Data INNER JOIN Cities ON Weather_Data.City=Cities.Id'):
        joined_data.append((row[0], row[1], row[2]))
    return joined_data

def avgCityTemp(data):
    avg_temps = []
    for item in data:
        temp = (item[0] + item[1]) / 2
        city = item[2]
        avg_temps.append((city, temp))
    
    citydict = defaultdict(list)
    for item in avg_temps:
        citydict[item[0]].append(item[1])
    citydict = dict(citydict)
    
    temp_means = []
    for temp in citydict.values():
        tempavg = statistics.mean(temp)
        temp_means.append(tempavg)

    cities = []
    for city in citydict:
        cities.append(city)

    citymeans = {}
    for i in range(len(cities)):
        citymeans[cities[i]] = temp_means[i]

    return citymeans

##############################


#### MAIN ####

def main():
    # collect data if necessary
    dataCollection()

    # connect to database
    cur, conn = databaseConnection('spotifyweather.db')

    #run calculations to find average popularity of each genre
    genreinfo = popularityGenre(cur, conn)
    genre_means = avgGenrePopularity(genreinfo)

    # run calculations to find average temperature of each city (in a given week)
    cityinfo = cityTemps(cur, conn)
    city_means = avgCityTemp(cityinfo)

if __name__ == "__main__":
    main()
