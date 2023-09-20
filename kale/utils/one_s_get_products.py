import requests

username = "kaleapi"
password = "kaleapi"


def get_products():
    url = "http://94.158.52.249/Base/hs/info/stocks/"
    # try:
    response = requests.get(url, auth=(username, password))
    return response.json()
    # except:
    #     sent_sms_base(105, "Error berdi", '+998901321921')
    #     return {"Товары": []}


def get_product_photo(code):
    url = f"http://94.158.52.249/Base/hs/info/foto?code={code}"
    response = requests.get(url, auth=(username, password))
    data = response.json()
    base64Photo = data.get('Фото')
    if base64Photo is None:
        return None
    return "data:image/png;base64," + base64Photo.replace("\r", '').replace("\n", '').replace("\'", '')
