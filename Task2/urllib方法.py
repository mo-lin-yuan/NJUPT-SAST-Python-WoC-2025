import urllib.request
import urllib.parse
import json
import time
import pandas as pd

def xiaomi():
    base_url = "https://api2.order.mi.com/rec/search"

    params = {
        "api": "/rec/search",
        "commodity_ids": "",
        "t": int(time.time())
    }

    query_string = urllib.parse.urlencode(params)

    full_url = base_url + "?" + query_string

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "Referer": "https://www.mi.com/"
    }

    req = urllib.request.Request(full_url, headers=headers)

    with urllib.request.urlopen(req) as response:
        result = response.read().decode("utf-8")
        data = json.loads(result)

    # print(data)
    data_list = data["data"]
    goods = []

    for item in data_list:
        info = item["info"]
        goods.append({
            "商品名称": info["name"],
            "价格": info["price"],
            "评论数": info["comments"],
            "图片": info["image"]
        })

    df=pd.DataFrame(goods)
    df.to_csv("urllib方法.csv", index=False, encoding="utf-8-sig")

    print("爬取完成，共", len(goods), "条")

xiaomi()