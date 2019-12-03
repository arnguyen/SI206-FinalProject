import requests

endpoint_url = "https://api.spotify.com/v1/recommendations?"

# OUR FILTERS
limit=10
market="US"
seed_genres="indie"
target_danceability=0.9

query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}'

response = requests.get(query, 
               headers={"Content-Type":"application/json", 
                        "Authorization": 'Bearer BQAwVFrXCjR-gzB37GenZFVDr4yETlE_rNWMK72kZFCLiJ39N13y9GEx4eZIJE05u3j6Nxc_GGqMV4UTEAwEHk3e0--IqtYFbPT2uN5sRouFrfs11_Bu6rV357S1ZfKxY7Hk7MZ1yoAW2uzVnL7tTiil9ypuZXq4wA4'})

json_response = response.json()
uris = []

for i in json_response['tracks']:
            uris.append(i)
            print(f"\"{i['name']}\" by {i['artists'][0]['name']}")
