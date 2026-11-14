import csv
import random
import re
import time
from datetime import datetime, timezone, timedelta

import instaloader

MAX_LINKS = 20

L = instaloader.Instaloader(
    quiet=True,
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    save_metadata=False,
    compress_json=False,
)


def shortcode(url):
    m = re.search(r"/(?:reel|reels|p|tv)/([A-Za-z0-9_-]+)", url)
    return m.group(1) if m else None


def fetch(code):
    post = instaloader.Post.from_shortcode(L.context, code)
    views = post.video_play_count or post.video_view_count or ""
    likes = "hidden" if post.likes < 0 else post.likes
    return views, likes, post.comments


def main():
    with open("links.txt") as f:
        links = [line.strip() for line in f if line.strip()][:MAX_LINKS]

    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist).strftime("%d %b %Y, %H:%M IST")
    rows = [["Reel link", "Views", "Likes", "Comments", "Updated", "Status"]]

    for url in links:
        code = shortcode(url)
        if not code:
            rows.append([url, "", "", "", now, "Invalid link"])
            continue
        try:
            views, likes, comments = fetch(code)
            rows.append([url, views, likes, comments, now, "OK"])
        except Exception as e:
            rows.append([url, "", "", "", now, type(e).__name__])
        time.sleep(random.uniform(5, 10))

    with open("results.csv", "w", newline="") as f:
        csv.writer(f).writerows(rows)


if __name__ == "__main__":
    main()
