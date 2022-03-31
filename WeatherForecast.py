import requests
import sys
from datetime import datetime

appid = "4aa4913f55ee689b48f7dddbfaf57b43"
smiles = {"overcast clouds": "☁",
          "broken clouds": "🌤",
          "scattered clouds": "⛅",
          "облачно с прояснениями": "⛅",
          "light rain": "🌧",
          "moderate rain": "🌧",
          "rain": "🌧",
          "light snow": "❄",
          "snow": "❄",
          "ясно": "☀"}
directions = {"S ": "South", "WS": "Southwest", "SE": "Southeast",
              "N ": "North", "NW": "Northwest", "NE": "Northeast",
              " W": "West", " E": "East"}


def get_wind_direction(deg):
    global res
    direction = ['N ', 'NE', ' E', 'SE', 'S ', 'WS', ' W', 'NW']
    for i in range(0, 8):
        step = 45.
        minimum = i * step - 45 / 2.
        maximum = i * step + 45 / 2.
        if i == 0 and deg > 360 - 45 / 2.:
            deg = deg - 360
        if minimum <= deg <= maximum:
            res = direction[i]
            break
    return res


def get_city_id(city_name):
    global city_identifier
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city_name, 'type': 'like', 'units': 'metric', 'lang': 'eng', 'APPID': appid})
        data = res.json()
        city_identifier = data['list'][0]['id']
    except Exception as e:
        print("Exception (find):", e)
        pass
    assert isinstance(city_identifier, int)
    return city_identifier


def request_forecast_today(id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': id, 'units': 'metric', 'lang': 'eng', 'APPID': appid})
        data = res.json()
        forecast = ""
        for i in data['list']:
            if int(i['dt_txt'][8:-9]) != datetime.now().day:
                break
            forecast += "{} {}{} {}{}".format(i['dt_txt'][11:16],
                                              smiles[i['weather'][0]['description']],
                                              '{0:+3.0f}'.format(i['main']['temp']) + "°C,",
                                              directions[get_wind_direction(i['wind']['deg'])],
                                              '{0:2.0f}'.format(i['wind']['speed']) + " m/s\n")
        return forecast
    except Exception as e:
        print("Exception (forecast):", e)
        pass


def request_forecast_tomorrow(id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': id, 'units': 'metric', 'lang': 'eng', 'APPID': appid})
        data = res.json()
        forecast = ""
        for i in data['list']:
            if int(i['dt_txt'][8:-9]) == datetime.now().day:
                continue
            if int(i['dt_txt'][8:-9]) == datetime.now().day + 1 or (int(i['dt_txt'][5:7]) != datetime.now().month and int(i['dt_txt'][8:-9]) == 1):
                forecast += "{} {}{} {}{}".format(i['dt_txt'][11:16],
                                                  smiles[i['weather'][0]['description']],
                                                  '{0:+3.0f}'.format(i['main']['temp']) + "°C,",
                                                  directions[get_wind_direction(i['wind']['deg'])],
                                                  '{0:2.0f}'.format(i['wind']['speed']) + " m/s\n")
            else:
                break
        return forecast
    except Exception as e:
        print("Exception (forecast):", e)
        pass


def request_forecast_five(id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': id, 'units': 'metric', 'lang': 'eng', 'APPID': appid})
        data = res.json()
        forecast = ""
        for i in data['list']:
            if i['dt_txt'][11:] == "15:00:00":
                forecast += "{}/{} {}{} {}{}".format(i['dt_txt'][8:10], i['dt_txt'][5:7],
                                                     smiles[i['weather'][0]['description']],
                                                     '{0:+3.0f}'.format(i['main']['temp']) + "°C,",
                                                     directions[get_wind_direction(i['wind']['deg'])],
                                                     '{0:2.0f}'.format(i['wind']['speed']) + " m/s\n")
        return forecast
    except Exception as e:
        print("Exception (forecast):", e)
        pass


if len(sys.argv) == 2:
    s_city_name = sys.argv[1]
    print("city:", s_city_name)
    city_id = get_city_id(s_city_name)
elif len(sys.argv) > 2:
    print('Enter name of city as one argument. For example: Kiev,UA')
    sys.exit()


print(request_forecast_tomorrow(get_city_id("Kiev")))