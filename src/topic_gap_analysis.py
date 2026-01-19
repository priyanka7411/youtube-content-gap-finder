def identify_topic_gaps(topic_counts: dict, total_videos: int) -> list:
    """
    Identify under-covered topics based on coverage ratio.
    Returns a list of topic gap dictionaries.
    """

    gaps = []

    if total_videos == 0:
        return gaps

    for topic, count in topic_counts.items():
        coverage_ratio = count / total_videos

        if coverage_ratio < 0.20:
            gaps.append({
                "topic": topic,
                "count": count,
                "coverage": round(coverage_ratio, 2)
            })

    # Sort gaps: lowest coverage first
    gaps.sort(key=lambda x: x["coverage"])

    return gaps
