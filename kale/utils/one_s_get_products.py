import requests

from config.settings.base import env

username = "kaleapi"
password = "kaleapi"


def get_products():
    url = "http://94.158.52.249/Base/hs/info/stocks/"
    try:
        response = requests.get(url, auth=(username, password))
        return response.json()
    except:
        return {"Товары": []}


def get_latest_update_datetime():
    url = "http://94.158.52.249/Base/hs/info/stocksChangeDate/"
    try:
        response = requests.get(url, auth=(username, password))
        json_data = response.json()
        return json_data
    except:
        return {"Товары": []}
