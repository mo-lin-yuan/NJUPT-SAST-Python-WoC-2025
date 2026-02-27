from playwright.sync_api import sync_playwright
import time
import random
import pandas as pd

def xiaomi_playwright():

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            page.goto("https://www.mi.com", timeout=60000)
            time.sleep(random.uniform(2, 4))

            result = page.evaluate("""
            fetch("https://api2.order.mi.com/rec/search?api=/rec/search&commodity_ids=&t=" + Math.floor(Date.now()/1000))
            .then(res => res.json())
            """)

            data_list = result.get("data", [])

            if not data_list:
                print("数据为空")
                browser.close()
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
            df.to_csv("playwright方法.csv", index=False, encoding="utf-8-sig")

            browser.close()

        print("爬取完成，共", len(df), "条")

    except Exception as e:
        print("请求异常:", e)

xiaomi_playwright()