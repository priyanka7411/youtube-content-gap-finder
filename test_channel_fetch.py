from src.youtube_api import fetch_channel_videos

videos = fetch_channel_videos(
    "https://www.youtube.com/@ankurwarikoo",
    max_results=10
)

print(f"Fetched {len(videos)} videos:")
for v in videos:
    print("-", v["title"])
