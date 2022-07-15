import requests
import config

currencies_list = {"USD": "🇺🇸", "EUR": "🇪🇺", "PLN": "🇵🇱"}
currency_code = {980: "UAH", 978: "EUR", 840: "USD"}
currency_code_smile = {980: "₴", 978: "€", 840: "$"}


def nbu_get_rate_info():
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


def apilayer_currency_converter(cur_to, cur_from, amount):
    try:
        res = requests.get("https://api.apilayer.com/currency_data/convert",
                           params={"to": cur_to, "from": cur_from, "amount": amount},
                           headers={"apikey": "knlzYGqMiwjZCU7nFiC4p4h5QjYULFfX"})
        data = res.json()
        return data["result"]
    except Exception as e:
        print("Exception (find):", e)
        pass


def mono_get_client_info():
    try:
        res = requests.get("https://api.monobank.ua/personal/client-info", headers={'X-Token': config.monobankToken})
        data = res.json()
        answer = "⚫ MonoBank:\n\n"
        for j in config.IBANs:
            for i in data["accounts"]:
                if i["iban"] == j:
                    answer += "{} {}: {} {}\n".format(i["type"].capitalize(), currency_code[i["currencyCode"]], i["balance"] / 100, currency_code_smile[i["currencyCode"]])
        return answer
    except Exception as e:
        print("Exception (find):", e)
        pass


def mono_past_webhook():
    data = requests.post("https://api.monobank.ua/personal/webhook", headers={"X-Token": config.monobankToken})
    return data


def mono_get_extract():
    try:
        res = requests.get("https://api.monobank.ua/personal/statement/{}/{}".format(0, 1654041600),
                           headers={'X-Token': config.monobankToken})
        data = res.json()
        return data
    except Exception as e:
        print("Exception (find):", e)
        pass


# print(apilayer_currency_converter("UAH", "USD", 50))
