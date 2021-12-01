import requests


currencies_list = {"USD": "🇺🇸", "EUR": "🇪🇺", "RUB": "🇷🇺"}


def get_rate_info():
    try:
        rates = ""
        for currency in currencies_list.keys():
            res = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange",
                               params={"valcode": currency, "": "json"})
            data = res.json()
            rates += "{} {}: {}\n".format(currencies_list[currency], data[0]['cc'], round(data[0]['rate'], 2))
        return rates
    except Exception as e:
        print("Exception (find):", e)
        pass


get_rate_info()
