import requests

from api.auth.send_sms_func import sent_sms_base
from config.settings.base import env

username = "kaleapi"
password = "kaleapi"


def get_products():
    url = "http://94.158.52.249/Base/hs/info/stocks/"

    sent_sms_base(105, f"Zapros ketdi {username} {password}", '+998901321921')
    try:
        response = requests.get(url, auth=(username, password))

        sent_sms_base(105, f"Status {response.status_code}", '+998901321921')
        return response.json()
    except:
        sent_sms_base(105, "Error boldi", '+998901321921')
        return {"Товары": []}


def get_latest_update_datetime():
    url = "http://94.158.52.249/Base/hs/info/stocksChangeDate/"
    try:
        response = requests.get(url, auth=(username, password))
        json_data = response.json()
        return json_data
    except:
        return {"Товары": []}
