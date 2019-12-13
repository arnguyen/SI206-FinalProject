import spotifyCollection
import weather
import sqlite3
import os
import sys
import requests
from collections import defaultdict
import statistics
import json

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


#### Function to aid user interface ####

def user_response():
    usr_response = input("Successful data processing! Would you like to process again? [y/n]")
    if usr_response.lower() == 'y':
        return main()
    elif usr_response.lower() == "n":
        print("Thanks for your time!")
        return
    else:
        print("Invalid input. Please try again.")
        return user_response()

############################


#### Connect to database ####

def databaseConnection(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

##############################


#### Function for writing to file ####

def writeData(filename, data):
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close()

##############################


#### Calculations for popularity and genre ####

def popularityGenre(cur, conn):
    joined_data = []
    for row in cur.execute('SELECT Tracks.Popularity, Genres.Title FROM Tracks INNER JOIN Genres ON Tracks.genre_id=Genres.genre_id'):
        joined_data.append((row[0], row[1]))
    return joined_data

def genrePopularities(data):
    genredict = defaultdict(list)
    for item in data:
        genredict[item[1]].append(item[0])
    genredict = dict(genredict)
    return genredict

def sortPopularities(data):
    genredict = genrePopularities(data)

    for genre in genredict:
        genredict[genre].sort()

    return genredict

def findValues(data):
    genredict = sortPopularities(data)

    five_summary = []
    for popularities in genredict.values():
        midindex = int(len(popularities) / 2)

        minpop = popularities[0]
        first_quart = statistics.median(popularities[:midindex])
        median_pop = statistics.median(popularities)
        third_quart = statistics.median(popularities[midindex + 1:])
        maxpop = popularities[-1]
        
        five_summary.append((minpop, first_quart, median_pop, third_quart, maxpop))
    
    genres = []
    for genre in genredict:
        genres.append(genre)

    genre_summary = {}
    for i in range(len(genres)):
        genre_summary[genres[i]] = five_summary[i]

    return genre_summary

def avgGenrePopularity(data):
    genredict = genrePopularities(data)

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

def getForecasts(cur, conn):
    forecasts = []
    for row in cur.execute('SELECT Description FROM Weather_Data'):
        forecasts.append(row[0])
    return forecasts

def forecastFreq(data):
    forecast_freq = {}
    for forecast in data:
        forecast_freq[forecast] = forecast_freq.get(forecast, 0) + 1
    return forecast_freq

def calculatemeans(data):
    citydict = defaultdict(list)
    for item in data:
        citydict[item[0]].append(item[1])
    citydict = dict(citydict)

    temp_means = []
    for temp in citydict.values():
        tempavg = statistics.mean(temp)
        temp_means.append(tempavg)
    for i in range(len(temp_means)):
        temp_means[i] = temp_means[i] * (9/5) - 459.67

    cities = []
    for city in citydict:
        cities.append(city)

    citymeans = {}
    for i in range(len(cities)):
        citymeans[cities[i]] = temp_means[i]
    
    return citymeans

def avgLowTemp(data):
    low_temps = []
    for item in data:
        city = item[2]
        temp = item[0]
        low_temps.append((city, temp))

    citylows = calculatemeans(low_temps)

    return citylows

def avgHighTemp(data):
    high_temps = []
    for item in data:
        city = item[2]
        temp = item[1]
        high_temps.append((city, temp))
    
    cityhighs = calculatemeans(high_temps)

    return cityhighs

##############################


#### MAIN ####

def main():
    # collect data if necessary
    try:
        dataCollection()
    except:
        print("Error occured in data collection. Please make sure access code is updated and try again.")
        return 

    # connect to database
    cur, conn = databaseConnection('spotifyweather.db')

    # run calculations to find average popularity of each genre
    genreinfo = popularityGenre(cur, conn)

    genre_means = avgGenrePopularity(genreinfo)
    writeData('genrepopularity.txt', genre_means)

    # run calculations to find box plot values for each genre
    #five_summary = findValues(genreinfo)
    #writeData('genresummary.txt', five_summary)
    boxplotdata = sortPopularities(genreinfo)
    writeData('genresummary.txt', boxplotdata)

    # run calculations to find average temperatures of each city (in a given week)
    cityinfo = cityTemps(cur, conn)

    low_means = avgLowTemp(cityinfo)
    writeData('avglowtemp.txt', low_means)

    high_means = avgHighTemp(cityinfo)
    writeData('avghightemp.txt', high_means)

    # run calculations to find frequency of each weather forecast
    forecasts = getForecasts(cur, conn)
    forecast_freq = forecastFreq(forecasts)
    writeData('forecastfreq.txt', forecast_freq)
    
    user_response()

    return

if __name__ == "__main__":
    main()