import requests
import pandas as pd
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch(start, headers, url):

    params = {
        "type": "10",
        "interval_id": "100:90",
        "action": "",
        "start": start,
        "limit": "20"
    }

    try:
        time.sleep(random.uniform(0.5, 1.5))

        res = requests.get(url, headers=headers, params=params, timeout=10)

        if res.status_code != 200:
            print(f"请求失败，状态码：{res.status_code}")
            return []

        if "application/json" not in res.headers.get("Content-Type", ""):
            print(f"返回内容不是JSON")
            return []

        data = res.json()

        if not data:
            return None

        return data

    except Exception as e:
        print(f"抓取异常：{e}")
        return []

def douban():
    total_start = time.perf_counter()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    }

    url = "https://movie.douban.com/j/chart/top_list"
    all_movies = []
    spider_start = time.perf_counter()

    starts = list(range(0, 10000, 20))

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fetch, start, headers, url): start for start in starts}

        for future in as_completed(futures):
            data = future.result()

            if data is None:
                print("抓到空数据，停止抓取")
                for f in futures:
                    if not f.done():
                        f.cancel()
                break

            for movie in data:
                all_movies.append({
                    "排名(rank)": movie.get("rank"),
                    "电影ID(id)": movie.get("id"),
                    "电影名称(title)": movie.get("title"),
                    "评分(score)": movie.get("score"),
                    "评分人数(vote_count)": movie.get("vote_count"),
                    "上映日期(release_date)": movie.get("release_date"),
                    "类型(types)": ",".join(movie.get("types", [])),
                    "地区(regions)": ",".join(movie.get("regions", [])),
                    "主演(actors)": ",".join(movie.get("actors", [])),
                    "主演人数(actor_count)": movie.get("actor_count"),
                    "是否可播放(is_playable)": movie.get("is_playable"),
                    "是否已观看(is_watched)": movie.get("is_watched"),
                    "封面接(cover_url)": movie.get("cover_url"),
                    "详情页链接(url)": movie.get("url")
                })

            print(f"目前共{len(all_movies)}部电影数据")

    all_movies.sort(key=lambda x: x["排名(rank)"])

    spider_end = time.perf_counter()
    save_start = time.perf_counter()

    df = pd.DataFrame(all_movies)
    df.to_csv("豆瓣电影悬疑片排行(加速版结果).csv", index=False, encoding="utf-8-sig")

    save_end = time.perf_counter()
    total_end = time.perf_counter()

    print(f"\n共爬取 {len(all_movies)} 部电影")
    print(f"爬取耗时：{spider_end - spider_start:.2f} 秒")
    print(f"保存耗时：{save_end - save_start:.2f} 秒")
    print(f"总耗时：{total_end - total_start:.2f} 秒")

for i in range(5):
    print(f'第{i}次数据')
    douban()