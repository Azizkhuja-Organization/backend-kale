import requests

from api.auth.send_sms_func import sent_sms_base

username = "kaleapi"
password = "kaleapi"


def get_products():
    url = "http://94.158.52.249/Base/hs/info/stocks/"
    # try:
    response = requests.get(url, auth=(username, password))
    sent_sms_base(105, response.status_code, '+998901321921')
    print(response.status_code)
    print(response.json())
    return response.json()
    # except:
    #     sent_sms_base(105, "Error berdi", '+998901321921')
    #     return {"Товары": []}
