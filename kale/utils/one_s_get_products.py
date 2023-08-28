import requests

from api.auth.send_sms_func import sent_sms_base

username = "kaleapi"
password = "kaleapi"


def get_products():
    url = "http://94.158.52.249/Base/hs/info/stocks/"
    sent_sms_base(105, "Zapros ketdi", '+998901321921')
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        sent_sms_base(105, "Error while updating products in kale", '+998901321921')


def get_latest_update_datetime():
    url = "http://94.158.52.249/Base/hs/info/stocksChangeDate/"
    try:
        response = requests.get(url, auth=(username, password))
        json_data = response.json()
        return json_data
    except:
        return {"Товары": []}
