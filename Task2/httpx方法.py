import httpx
import time
import pandas as pd

def xiaomi():
    url = "https://www.mi.com/"
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

    with httpx.Client() as client:
        response = client.get(url, params=params, headers=headers)
        data = response.json()

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

    df = pd.DataFrame(goods)
    df.to_csv("httpx法.csv", index=False, encoding="utf-8-sig")

    print("爬取完成，共", len(goods), "条")

xiaomi()