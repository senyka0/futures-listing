import json
import requests
from bs4 import BeautifulSoup
import time

url = "https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48"
last_event_id = None
finandy_key = "" # your key

def execute(symbol):
    data = {
        "name": "Hook 201083",# hook name
        "secret": "0tw9zls87c",# hook secret
        "side": "buy",
        "symbol": f"{symbol}USDT",
        "sl": {
            "enabled": True,
            "ofsMode": "pos",
            "ofs": "5"
        },
        "tp": {
            "enabled": True,
            "orders": [
                {
                    "ofs": "5"
                }
            ]
        },
        "open": {
            "amountType": "sumUsd",
            "amount": "100" # trade amount
        }
    }
    res = requests.post(f"https://hook.finandy.com/{finandy_key}",
                        data=json.dumps(data), headers={"Content-Type": "application/json"})
    print(res.json())


def main():
    try:
        global last_event_id
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        event = json.loads(soup.find("script", {"id": "__APP_DATA"}).text)
        new = event["routeProps"]["ce50"]["catalogs"][0]["articles"][0]

        if last_event_id == None:
            last_event_id = new["id"]
            return

        if new["id"] != last_event_id:
            last_event_id = new["id"]
            if new["title"].startswith("Binance Futures Will Launch USDⓈ-M ") and "Perpetual Contract with Up to 20X Leverage" in new["title"]:
                token = new["title"].split(
                    "Binance Futures Will Launch USDⓈ-M")[1].split(" ")[1]
                execute(token)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(5)
