import requests
import pandas as pd
import time

def douban():
    total_start = time.perf_counter()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    }

    url = "https://movie.douban.com/j/chart/top_list"

    all_movies = []

    spider_start = time.perf_counter()

    base_params = {
        "type": "10",
        "interval_id": "100:90",
        "action": "",
        "limit": "20"
    }

    for start in range(0, 10000, 20):
        base_params["start"] = start

        res = requests.get(url, headers=headers, params=base_params,timeout=10)

        if res.status_code != 200:
            print("请求失败，停止爬取")
            break

        if "application/json" not in res.headers.get("Content-Type", ""):
            print("返回内容不是JSON")
            break

        data = res.json()

        if not data:
            print("数据为空，停止爬取")
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

        print(f"第{start//20 + 1}次完成，目前共{len(all_movies)}部电影")

        time.sleep(1)

    spider_end = time.perf_counter()
    save_start = time.perf_counter()

    df = pd.DataFrame(all_movies)

    df.to_csv("豆瓣电影悬疑片排行(基础版结果).csv", index=False, encoding="utf-8-sig")

    save_end = time.perf_counter()
    total_end = time.perf_counter()

    print(f"\n共爬取{len(all_movies)}部电影")
    print(f"爬取耗时：{spider_end - spider_start:.2f} 秒")
    print(f"保存耗时：{save_end - save_start:.2f} 秒")
    print(f"总耗时：{total_end - total_start:.2f} 秒")

douban()
