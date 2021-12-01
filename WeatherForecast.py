import requests
import sys
from datetime import datetime

appid = "54136453698981eea1430cbee65e00a3"
smiles = {"небольшая облачность": "🌤", "переменная облачность": "⛅", "небольшой снег": "❄", "пасмурно": "☁"}
directions = {"Ю": "Юг", "ЮЗ": "Юго-Запад", "ЮВ": "Юго-Восток",
              "С": "Север", "СЗ": "Северо-Запад", "СВ": "Северо-Восток",
              " З": "Запад", "В": "Восток"}


def get_wind_direction(deg):
    direction = ['С ', 'СВ', ' В', 'ЮВ', 'Ю ', 'ЮЗ', ' З', 'СЗ']
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
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
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
                           params={'id': id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        forecast = ""
        for i in data['list']:
            if int(i['dt_txt'][8:-9]) != datetime.now().day:
                break
            forecast += "{} {}{} {}{}".format(i['dt_txt'][11:16],
                                              smiles[i['weather'][0]['description']],
                                              '{0:+3.0f}'.format(i['main']['temp']) + "°C,",
                                              directions[get_wind_direction(i['wind']['deg'])],
                                              '{0:2.0f}'.format(i['wind']['speed']) + " м/с\n")
        return forecast
    except Exception as e:
        print("Exception (forecast):", e)
        pass


if len(sys.argv) == 2:
    s_city_name = sys.argv[1]
    print("city:", s_city_name)
    city_id = get_city_id(s_city_name)
elif len(sys.argv) > 2:
    print('Enter name of city as one argument. For example: Petersburg,RU')
    sys.exit()