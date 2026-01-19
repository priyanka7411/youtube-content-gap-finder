def cluster_topics(videos: list) -> dict:
    """
    Assign each video to a topic based on keyword rules.
    Returns a dictionary of topic -> count.
    """

    topic_rules = {
        "investing": ["sip", "mutual fund", "invest", "investment"],
        "stock_market": ["stock", "trading", "shares", "equity"],
        "personal_finance": ["budget", "saving", "expense", "money habit"],
        "taxation": ["tax", "gst", "income tax", "itr"],
        "debt": ["loan", "credit card", "emi", "debt"],
        "insurance": ["insurance", "term plan", "health insurance"],
        "income": ["salary", "income", "side income", "passive income"],
        "retirement": ["retirement", "pension", "pf", "nps"],
    }

    topic_counts = {topic: 0 for topic in topic_rules}

    for video in videos:
        text = (
            f"{video.get('title', '')} "
            f"{video.get('description', '')}"
        ).lower()

        for topic, keywords in topic_rules.items():
            if any(keyword in text for keyword in keywords):
                topic_counts[topic] += 1
                break  # one primary topic per video

    return topic_counts
