import sqlite3
import os
import requests
import sys

#### Deals with API ####

def read_access_token():
    """ Reads access token written from spotifyOauth.py """

    f = open('accesstoken.txt', 'r')
    access_token = f.read()
    f.close()
    return access_token

def check_access_token(access_token):
    """ Connects to api using random parameters to check that the access token works """
    
    endpoint_url = "https://api.spotify.com/v1/recommendations?"

    # FILTERS
    limit=1    
    market="US"
    seed_genres="indie"

    query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}'

    response = requests.get(query, headers={"Content-Type":"application/json", "Authorization": 'Bearer ' + access_token})
    json_response = response.json()
    
    return json_response

############################


#### Deals with Database ####

def setUpDatabase(db_name):
    """ Sets up database """

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpGenreTable(data, cur, conn):
    """ Sets up Genre Table """
    
    cur.execute('''CREATE TABLE IF NOT EXISTS Genres (genre_id INTEGER PRIMARY KEY, Title TEXT)''')

    if cur.execute('SELECT Title FROM Genres WHERE Title = ?', (data[0][-1], )).fetchone() != None:
        print(data[0][-1] + ' has already been added to Genres.')
        return
        
    try:
        cur.execute("INSERT INTO Genres (Title) VALUES (?)", (data[0][-1],))
        print("Successful Genre Insertion!")
    except:
        print("Error in Genre Insertion")
    conn.commit()

def setUpTrackTable(data, cur, conn):
    """ Sets up Track table """

    genre_ids = {}
    cur.execute("SELECT genre_id, Title FROM Genres")
    result = cur.fetchall()
    for genre_id, title in result:
        genre_ids[title] = genre_id

    cur.execute('''CREATE TABLE IF NOT EXISTS Tracks (track_id TEXT PRIMARY KEY, Title TEXT, Album TEXT, Artist TEXT, Popularity INTEGER, genre_id INTEGER)''') 
    for track in data:
        if cur.execute('SELECT track_id FROM Tracks WHERE track_id = ?', (track[0], )).fetchone() != None:
            print(track[0] + ' has already been added to Tracks.')
            continue
        try:
            cur.execute("INSERT INTO Tracks (track_id, Title, Album, Artist, Popularity, genre_id) VALUES (?,?,?,?,?,?)", (track[0], track[1], track[2], track[3], track[4], genre_ids[track[5]]))
            print("Successful Track Insertion!")
        except:
            print("Error in Track Insertion") 
    conn.commit()

############################


#### Function to aid user interface ####

def user_response():
    usr_response = input("Would you like to enter another genre? [y/n]")
    if usr_response.lower() == 'y':
        return main()
    elif usr_response.lower() == "n":
        return
    else:
        print("Invalid input. Please try again.")
        return user_response()

############################


#### Class for Data Collection ####

class DataCollection:
    def __init__(self, genre, access_token):
        self.genre = genre
        self.access_token = access_token
        self.data = []
    
    def getData(self):
        return self.data

    def collectData(self):
        """ Connects to api, fills self.data with lists of track info """

        endpoint_url = "https://api.spotify.com/v1/recommendations?"

        # FILTERS
        limit=20    
        market="US"
        seed_genres=self.genre
        access_token=self.access_token

        query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}'

        response = requests.get(query, headers={"Content-Type":"application/json", "Authorization": 'Bearer ' + access_token})
        json_response = response.json()

        for i in json_response['tracks']:
            track_info = []
            track_info.append(i['id'])
            track_info.append(i['name'])
            track_info.append(i['album']['name'])
            track_info.append(i['artists'][0]['name'])
            track_info.append(i['popularity'])
            track_info.append(seed_genres)           
            self.data.append(track_info)
        
        return json_response

############################
     

#### MAIN ####

def main():
    # read current access token and check if it connects
    try:
        access_token = read_access_token()
        json_response = check_access_token(access_token)
        if list(json_response.keys())[0] == 'error':
            if json_response['error']['status'] == 401:
                raise Exception
    # if it's expired, run the authorization to get a new access code
    except:
        print("Access code expired, getting new access code")
        import spotifyOauth 
        access_token = read_access_token()
    
    # run data collection
    genre = input("Pick a Genre: ")
    genre_collector = DataCollection(genre, access_token)
    json_response = genre_collector.collectData()
    if len(json_response['tracks']) == 0:
        print("Invalid Genre. Please Try Again")
        return main()
    genre_data = genre_collector.getData()

    # set up database
    cur, conn = setUpDatabase('spotifyweather.db')

    # set up tables
    setUpGenreTable(genre_data, cur, conn)
    setUpTrackTable(genre_data, cur, conn)

    user_response()

    return   

if __name__ == "__main__":
    main()