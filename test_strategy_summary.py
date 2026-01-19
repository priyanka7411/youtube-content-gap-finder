from src.youtube_api import fetch_channel_videos
from src.intent_analysis import extract_intent_counts
from src.topic_clustering import cluster_topics
from src.topic_gap_analysis import identify_topic_gaps
from src.strategy_summary import generate_strategy_summary

CHANNEL_URL = "https://www.youtube.com/@warikoo"

videos = fetch_channel_videos(CHANNEL_URL, max_results=20)

intent_counts = extract_intent_counts(videos)
topic_counts = cluster_topics(videos)
topic_gaps = identify_topic_gaps(topic_counts, total_videos=len(videos))

summary = generate_strategy_summary(
    intent_counts=intent_counts,
    topic_counts=topic_counts,
    topic_gaps=topic_gaps,
    total_videos=len(videos)
)

print("\nChannel Strategy Summary:\n")
for line in summary:
    print("-", line)
