import requests

from api.auth.send_sms_func import sent_sms_base

username = "kaleapi"
password = "kaleapi"


def get_products():
    url = "http://94.158.52.249/Base/hs/info/stocks/"
    response = requests.get(url, auth=(username, password))
    sent_sms_base(105, f"Zapros ketdi{response.status_code} {len(response.json().get('Товары'))}", '+998901321921')
    if response.status_code == 200:
        return response.json()
    else:
        sent_sms_base(105, "Error while updating products in kale", '+998901321921')
