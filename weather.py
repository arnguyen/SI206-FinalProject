import requests
import json
import sqlite3
import pprint


def getWeather(city_name):
    api_key = '0b0dc4f8f0b55df750805de1e44f7895'
    base_url = 'http://api.openweathermap.org/data/2.5/forecast?q='
    complete_url = base_url + city_name + '&appid=' + api_key
    get_data = requests.get(complete_url)
    data = get_data.json()
    return data



def getWeatherData(data):
    #conn = sqlite3.connect('Weather_db.sqlite')
    #cur = conn.cursor()
    #cur.execute('DROP TABLE IF EXISTS Weather_Data')
    #cur.execute('CREATE TABLE Weather_Data(Id TEXT, City TEXT, Time TEXT, Temp_Max INTEGER, Temp_Min INTEGER, Humidity INTEGER, Description TEXT)')
    _city_id = data['city']['id']
    _city_name = data['city']['name']
    count = 0 
    for city in data['list']:
        _time = city['dt_txt']
        _max_temp = city['main']['temp_max']
        _min_temp = city['main']['temp_min']
        _humidity = city['main']['humidity']
        _description = city['weather'][0]['description']
        count += 1
        if count == 17:
            break
        cur.execute('INSERT INTO Weather_Data(Id, City, Time, Temp_Max, Temp_Min, Humidity, Description) VALUES (?,?,?,?,?,?,?)', (_city_id, _city_name, _time, _max_temp, _min_temp, _humidity, _description))
        conn.commit()

        
conn = sqlite3.connect('Weather_db.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Weather_Data')
cur.execute('CREATE TABLE Weather_Data(Id TEXT, City TEXT, Time TEXT, Temp_Max INTEGER, Temp_Min INTEGER, Humidity INTEGER, Description TEXT)')

def main():
    cities = ['Boston', 'Chicago', 'Detroit', 'Los Angeles', 'Manhattan', 'Nashville', 'New Orleans', 'Oakland', 'Philadelphia', 'Seattle']
    
    for city in cities:
        weather = getWeather(city)
        getWeatherData(weather)

if __name__ == "__main__":
    main()
    #unittest.main(verbosity = 2)

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









    



