import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from googleapiclient.errors import HttpError

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in environment variables")

youtube = build("youtube", "v3", developerKey=API_KEY)


def fetch_channel_videos(channel_url: str, max_results: int = 20) -> list:
    """
    Fetch videos from a specific YouTube channel URL.
    """

    # 1. Extract channel ID
    if "@" in channel_url:
        handle = channel_url.split("@")[-1]

        request = youtube.search().list(
            q=handle,
            part="snippet",
            type="channel",
            maxResults=1
        )
        response = request.execute()

        if not response.get("items"):
            raise ValueError("Channel not found")

        channel_id = response["items"][0]["snippet"]["channelId"]

    elif "/channel/" in channel_url:
        channel_id = channel_url.split("/channel/")[-1]

    else:
        raise ValueError("Unsupported channel URL format")

    # 2. Fetch videos from channel
    request = youtube.search().list(
        channelId=channel_id,
        part="snippet",
        maxResults=min(max_results, 25),
        type="video",
        order="date"
    )

    response = request.execute()

    videos = []
    for item in response.get("items", []):
        snippet = item["snippet"]
        videos.append({
            "title": snippet["title"],
            "description": snippet["description"],
            "channel": snippet["channelTitle"]
        })

    return videos


def fetch_videos(keyword: str, max_results: int = 10) -> list:
    try:
        request = youtube.search().list(
            q=keyword,
            part="snippet",
            maxResults=min(max_results, 25),
            type="video"
        )

        response = request.execute()

    except HttpError as e:
        # Graceful failure for V1
        return []

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
