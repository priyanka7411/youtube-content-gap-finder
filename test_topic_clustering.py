
from data.sample_videos_v2 import sample_videos
from src.topic_clustering import cluster_topics
from src.topic_gap_analysis import identify_topic_gaps

if __name__ == "__main__":
    topic_counts = cluster_topics(sample_videos)
    total_videos = len(sample_videos)

    print("V2 Topic Counts:")
    for topic, count in topic_counts.items():
        print(f"{topic}: {count}")

    print("\nV2 Topic Gaps:")
    gaps = identify_topic_gaps(topic_counts, total_videos)

    for gap in gaps:
        print(
            f"{gap['topic']} → "
            f"{gap['count']} videos "
            f"({gap['coverage']*100:.0f}% coverage)"
        )
