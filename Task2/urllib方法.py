import urllib.request
import urllib.parse
import json
import time
import pandas as pd
import random

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

    try:
        time.sleep(random.uniform(0.5, 1.5))

        req = urllib.request.Request(full_url, headers=headers)

        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status != 200:
                print("请求失败")
                return

            result = response.read().decode("utf-8")
            data = json.loads(result)

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
        df.to_csv("urllib方法.csv", index=False, encoding="utf-8-sig")

        print("爬取完成，共", len(df), "条")

    except Exception as e:
        print("请求异常:", e)

xiaomi()