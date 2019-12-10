import sqlite3
import os
import requests
import sys

def read_access_token():
    """ Reads access token written from spotifyOauth.py """

    f = open('accesstoken.txt', 'r')
    access_token = f.read()
    return access_token

def check_access_token(access_token):
    """ Connects to api using random parameters to check that the access token works """
    
    endpoint_url = "https://api.spotify.com/v1/recommendations?"

    # OUR FILTERS
    limit=1    
    market="US"
    seed_genres="indie"

    query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}'

    response = requests.get(query, headers={"Content-Type":"application/json", "Authorization": 'Bearer ' + access_token})

def setUpDatabase(db_name):
    """ Sets up database """

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

class DataCollection:
    def __init__(self, genre, access_token):
        self.genre = genre
        self.access_token = access_token

    def collectData(self):
        endpoint_url = "https://api.spotify.com/v1/recommendations?"

        # OUR FILTERS
        limit=    
        market="US"
        seed_genres=self.genre
        access_token=self.access_token

        query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}'

        response = requests.get(query, headers={"Content-Type":"application/json", "Authorization": 'Bearer ' + access_token})
                                                 
        json_response = response.json()

        for i in json_response['tracks']:
            #uris.append(i['name'])
            #uris.append(i['artists'][0]['name'])
            print(f"\"{i['name']}\" by {i['artists'][0]['name']}")




def main():
    # read current access token and check if it connects
    try:
        access_token = read_access_token()
        check_access_token(access_token)
    # if it's expired, run the authorization to get a new access code
    except:
        print("exception")
        import spotifyOauth 
        access_token = read_access_token()
    
    # set up database
    cur, conn = setUpDatabase('spotify.db')
    
    # run data collection
    happy = DataCollection("happy", access_token)
    happy.collectData()

if __name__ == "__main__":
    main()