from bottle import route, run, request
import spotipy
from spotipy import oauth2
import requests
"""
PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = 'df18e7063143495994aae82d0aea9708'
SPOTIPY_CLIENT_SECRET = 'da3d58de003f4c61aabaa192aaa2c102'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

@route('/')
def index():
        
    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return results

    else:
        return htmlForLoginButton()

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

run(host='', port=8080)
"""





endpoint_url = "https://api.spotify.com/v1/recommendations?"

# OUR FILTERS
limit=20    
market="US"
seed_genres="indie"
target_danceability=0.9

query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}'

response = requests.get(query, 
               headers={"Content-Type":"application/json", 
                        "Authorization": 'Bearer AQA17CjxPqwRqt_s_GIz_nWUylCe-h1mjOeLSk5uiOeHuBRLXeLKcC87PURTuzFgqbU9HKfppV0cqr2DIQLbc9mqBIIYUJpNLApwOZPwjjmpFylZG1kxQdYHlLabUtoWVBdzfF4HEqAD2q8krVmAw7GcfPTo3THrekf8YroimFpkx1V4qFPMpG9_vWWAYBitVpYyDBcQgm2ij95xqPo'})
                                                 
json_response = response.json()
uris = []

for i in json_response['tracks']:
            uris.append(i)
            print(f"\"{i['name']}\" by {i['artists'][0]['name']}")

