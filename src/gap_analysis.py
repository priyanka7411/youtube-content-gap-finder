def identify_content_gaps(intent_counts: dict, total_videos: int, threshold: float = 0.15):
    """
    Identifies under-served intents.
    threshold = max % of videos that can mention intent to be considered a gap
    """

    gaps = []

    for intent, count in intent_counts.items():
        ratio = count / total_videos

        if ratio <= threshold:
            gaps.append({
                "intent": intent,
                "count": count,
                "ratio": round(ratio, 2)
            })

    return sorted(gaps, key=lambda x: x["ratio"])
