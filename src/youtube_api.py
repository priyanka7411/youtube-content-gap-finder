import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in environment variables")

youtube = build("youtube", "v3", developerKey=API_KEY)


def fetch_videos(keyword: str, max_results: int = 10) -> list:
    """
    Fetch basic YouTube video data for a given keyword.
    Returns a list of dictionaries.
    """

    request = youtube.search().list(
    q=keyword,
    part="snippet",
    maxResults=min(max_results, 25),
    type="video"
)


    response = request.execute()

    videos = []

    for item in response.get("items", []):
        snippet = item["snippet"]

        videos.append({
            "title": snippet["title"],
            "description": snippet["description"],
            "published_at": snippet["publishedAt"],
            "channel": snippet["channelTitle"]
        })

    return videos
