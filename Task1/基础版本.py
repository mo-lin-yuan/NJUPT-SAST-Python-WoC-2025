import requests

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
                "rank": movie.get("rank"),
                "id": movie.get("id"),
                "title": movie.get("title"),
                "score": movie.get("score"),
                "rating_value": movie.get("rating")[0] if movie.get("rating") else "",
                "rating_people": movie.get("rating")[1] if movie.get("rating") else "",
                "vote_count": movie.get("vote_count"),
                "cover_url": movie.get("cover_url"),
                "url": movie.get("url"),
                "release_date": movie.get("release_date"),
                "types": ",".join(movie.get("types", [])),  # 列表转字符串
                "regions": ",".join(movie.get("regions", [])),  # 列表转字符串
                "actors": ",".join(movie.get("actors", [])),  # 列表转字符串
                "actor_count": movie.get("actor_count"),
                "is_playable": movie.get("is_playable"),
                "is_watched": movie.get("is_watched")
            })

    print(f"\n共爬取 {len(all_movies)} 部电影")

douban()
