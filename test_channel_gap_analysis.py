from src.youtube_api import fetch_channel_videos
from src.intent_analysis import extract_intent_counts
from src.topic_clustering import cluster_topics
from src.topic_gap_analysis import identify_topic_gaps

CHANNEL_URL = "https://www.youtube.com/@warikoo"

videos = fetch_channel_videos(CHANNEL_URL, max_results=20)

print(f"\nAnalyzing {len(videos)} channel videos...\n")

intent_counts = extract_intent_counts(videos)
topic_counts = cluster_topics(videos)
topic_gaps = identify_topic_gaps(topic_counts, total_videos=len(videos))

print("Viewer Intent Coverage:")
for k, v in intent_counts.items():
    print(f"{k}: {v}")

print("\nTopic Coverage:")
for k, v in topic_counts.items():
    print(f"{k}: {v}")

print("\nTopic Gaps:")
for gap in topic_gaps:
    print(f"{gap['topic']} → {gap['count']} videos ({gap['coverage']}% coverage)")
