import spotifyCollection
import weather
import sqlite3
import os
import sys
import requests

def fillDatabase():
    for i in range(5):
        spotifyCollection.main()
        weather.main()

def databaseConnection(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def popularityGenre(cur, conn):
    joined_data = []
    for row in cur.execute('SELECT Tracks.Popularity, Genres.Title FROM Tracks INNER JOIN Genres ON Tracks.genre_id=Genres.genre_id'):
        joined_data.append((row[0], row[1]))
    return joined_data

def main():
    #fillDatabase()
    cur, conn = databaseConnection('spotifyweather.db')
    popularityGenre(cur, conn)

if __name__ == "__main__":
    main()
