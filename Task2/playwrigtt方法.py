from playwright.sync_api import sync_playwright
import time
import pandas as pd

def xiaomi_playwright():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.mi.com")
        time.sleep(3)

        result = page.evaluate("""
        fetch("https://api2.order.mi.com/rec/search?api=/rec/search&commodity_ids=&t=" + Math.floor(Date.now()/1000))
        .then(res => res.json())
        """)

        data_list = result["data"]

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
        df.to_csv("playwright方法.csv", index=False, encoding="utf-8-sig")

        browser.close()

xiaomi_playwright()