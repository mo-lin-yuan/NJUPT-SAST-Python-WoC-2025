import requests
import time
import pandas as pd

def xioami():
    url = "https://api2.order.mi.com/rec/search"

    params = {
        "api": "/rec/search",
        "commodity_ids": "",
        "t": int(time.time())
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "Referer": "https://www.mi.com/"
    }

    response = requests.get(url, params=params, headers=headers)

    # print(response.json())

    df=pd.DataFrame(response.json())
    df.to_csv("requests方法.csv", index=False, encoding="utf-8-sig")

xioami()