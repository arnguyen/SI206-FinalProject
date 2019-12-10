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
    json_response = response.json()
    
    return json_response

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
        self.data = []

    def collectData(self):
        endpoint_url = "https://api.spotify.com/v1/recommendations?"

        # OUR FILTERS
        limit=1    
        market="US"
        seed_genres=self.genre
        access_token=self.access_token

        query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}'

        response = requests.get(query, headers={"Content-Type":"application/json", "Authorization": 'Bearer ' + access_token})
                                                 
        json_response = response.json()
        track_info = []
        #print(json_response)

        for i in json_response['tracks']:
            track_info.append(i['id'])
            track_info.append(i['name'])
            track_info.append(i['album']['name'])
            track_info.append(i['artists'][0]['name'])
            track_info.append(i['popularity'])
            track_info.append(seed_genres)           
            self.data.append(track_info)
        

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
    
    # set up database
    cur, conn = setUpDatabase('spotify.db')
    
    # run data collection
    happy = DataCollection("indie", access_token)
    happy.collectData()
    print(happy.data)

if __name__ == "__main__":
    main()