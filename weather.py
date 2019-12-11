import requests
import json
import sqlite3
import pprint
import os

full_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'spotifyweather.db'
conn = sqlite3.connect(full_path)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Weather_Data(Id TEXT, City TEXT, Date TEXT , Time TEXT, Temp_Max INTEGER, Temp_Min INTEGER, Humidity INTEGER, Description TEXT)')
cur.execute("CREATE TABLE IF NOT EXISTS Cities (Id INTEGER PRIMARY KEY, City TEXT)")


def getWeather(city_name):
    api_key = '0b0dc4f8f0b55df750805de1e44f7895'
    base_url = 'http://api.openweathermap.org/data/2.5/forecast?q='
    complete_url = base_url + city_name + '&appid=' + api_key
    get_data = requests.get(complete_url)
    data = get_data.json()
    return data


def getCityTable(data):
    _city_name = data['city']['name']
    if cur.execute('SELECT City FROM Cities WHERE City = ?', (_city_name, )).fetchone() != None:
        print('City has already been added. Please try again.')
        return False
    cur.execute('INSERT INTO Cities (City) VALUES (?)',(_city_name, ))
    print("Successful City Insertion!")
    conn.commit()
    return True

def getWeatherTable(data):
    count = 0 
    
    city_ids = {}
    cur.execute("SELECT Id, City FROM Cities")
    result = cur.fetchall()
    for Id, City in result:
        city_ids[City] = Id
    
    _city_name = data['city']['name']
    _city_id = data['city']['id']
    for city in data['list']:
        _time_and_date = city['dt_txt']
        _date = _time_and_date.split()[0]
        _time = _time_and_date.split()[1]
        _max_temp = city['main']['temp_max']
        _min_temp = city['main']['temp_min']
        _humidity = city['main']['humidity']
        _description = city['weather'][0]['description']
        if count == 20:
            break
        cur.execute('INSERT INTO Weather_Data(Id, City, Date, Time, Temp_Max, Temp_Min, Humidity, Description) VALUES (?,?,?,?,?,?,?,?)', (_city_id, city_ids[_city_name], _date, _time, _max_temp, _min_temp, _humidity, _description))
        count += 1
    conn.commit()

#### Function to aid user interface ####

def user_response():
    usr_response = input("Would you like to enter another city? [y/n]")
    if usr_response.lower() == 'y':
        return main()
    elif usr_response.lower() == "n":
        print("Thanks for your time!")
        return
    else:
        print("Invalid input. Please try again.")
        return user_response()

############################

def main():
    city_name = input('Enter a city: ')
    weather = getWeather(city_name)
    if getCityTable(weather):
        getWeatherTable(weather)

    user_response()
    

if __name__ == "__main__":
    main()