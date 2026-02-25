import requests
import pandas as pd

def douban():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    }

    url = "https://movie.douban.com/j/chart/top_list"

    all_movies = []

    for start in range(0, 320, 20):
        params = {
            "type": "10",
            "interval_id": "100:90",
            "action": "",
            "start": start,
            "limit": "20"
        }

        res = requests.get(url, headers=headers, params=params)
        print(res.text)
        data = res.json()
        print(data)

        for movie in data:
            all_movies.append({
                "排名(rank)": movie.get("rank"),
                "电影ID(id)": movie.get("id"),
                "电影名称(title)": movie.get("title"),
                "评分(score)": movie.get("score"),
                "评分人数(vote_count)": movie.get("vote_count"),
                "上映日期(release_date)": movie.get("release_date"),
                "类型(types)": ",".join(movie.get("types", [])), # 列表转字符串
                "地区(regions)": ",".join(movie.get("regions", [])), # 列表转字符串
                "主演(actors)": ",".join(movie.get("actors", [])), # 列表转字符串
                "主演人数(actor_count)": movie.get("actor_count"),
                "是否可播放(is_playable)": movie.get("is_playable"),
                "是否已观看(is_watched)": movie.get("is_watched"),
                "封面接(cover_url)": movie.get("cover_url"),
                "详情页链接(url)": movie.get("url")
            })

    df = pd.DataFrame(all_movies)

    df.to_csv("豆瓣电影悬疑片排行.csv", index=False, encoding="utf-8-sig")

    print(f"\n共爬取 {len(all_movies)} 部电影")

douban()
