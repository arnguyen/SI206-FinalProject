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

'''
def getNameTable(city_name):
    city_list = []
    city_list = city_list.append(city_name)
    for x in range(len(city_list)):
        cur.execute('INSERT INTO Cities (Id,City) VALUES (?,?)',(x + 1 ,city_list[x]))
    conn.commit()
'''

def getCityTable(data):
    _city_name = data['city']['name']
    if cur.execute('SELECT City FROM Weather_Data WHERE City = ?', (_city_name, )).fetchone() != None:
        print('City is already added. Try a different city!')
        return
    cur.execute('INSERT INTO Cities (City) VALUES (?)',(_city_name, ))
    conn.commit()

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

def main():
    city_name = input('Enter a city: ')
    weather = getWeather(city_name)
    getCityTable(weather)
    getWeatherTable(weather)

    #getNameTable(city_name)
    

if __name__ == "__main__":
    main()

'''
Boston = 'Boston'
Boston_Weather = getWeather(Boston)
getWeatherData(Boston_Weather)

Chicago = 'Chicago'
Chicago_Weather = getWeather(Chicago)
getWeatherData(Chicago_Weather)

Detroit = 'Detroit'
Detroit_Weather = getWeather(Detroit)
getWeatherData(Detroit)

Los_Angeles = 'Los_Angeles'
LA_Weather = getWeather(Los_Angeles)
getWeatherData(LA_Weather)

Manhattan = 'Manhattan'
Manhattan_Weather = getWeather(Manhattan)
getWeatherData(Manhattan_Weather)

Nashville = 'Nashville'
Nashville_Weather = getWeather(Nashville)
getWeatherData(Nashville_Weather)

New_Orleans = 'New Orleans'
NO_Weather = getWeather(New_Orleans)
getWeatherData(NO_Weather)

Oakland = 'Oakland'
Oakland_Weather = getWeather(Oakland)
getWeatherData(Oakland_Weather)

Philadelphia = 'Philadelphia'
Philadelphia_Weather = getWeather(Philadelphia)
getWeatherData(Philadelphia_Weather)

Seattle = 'Seattle'
Seattle_Weather = getWeather(Seattle)
getWeatherData(Seattle_Weather)
'''









    



