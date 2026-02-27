import httpx
import time
import random
import pandas as pd

def xiaomi():
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

    try:
        time.sleep(random.uniform(0.5, 1.5))

        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, params=params, headers=headers)

        if response.status_code != 200:
            print("请求失败")
            return

        data = response.json()
        data_list = data.get("data", [])

        if not data_list:
            print("数据为空")
            return

        goods = []

        for item in data_list:
            info = item.get("info", {})
            goods.append({
                "商品名称": info.get("name"),
                "价格": info.get("price"),
                "评论数": info.get("comments"),
                "图片": info.get("image")
            })

        df = pd.DataFrame(goods).drop_duplicates()
        df.to_csv("httpx法.csv", index=False, encoding="utf-8-sig")

        print("爬取完成，共", len(df), "条")

    except Exception as e:
        print("请求异常:", e)

xiaomi()