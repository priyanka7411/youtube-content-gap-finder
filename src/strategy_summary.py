def generate_strategy_summary(
    intent_counts: dict,
    topic_counts: dict,
    topic_gaps: list,
    total_videos: int
) -> list:
    """
    Generate human-readable content strategy insights
    based on intent and topic analysis.
    """

    insights = []

    # -------- Intent-level insights --------
    if not intent_counts:
        insights.append(
            "The channel rarely addresses clear viewer questions "
            "like why, mistakes, or how-to explanations."
        )
    else:
        dominant_intents = sorted(
            intent_counts.items(), key=lambda x: -x[1]
        )

        top_intent, top_count = dominant_intents[0]

        if top_count / total_videos > 0.2:
            insights.append(
                f"The channel frequently uses '{top_intent}' style content, "
                "suggesting a focus on opinions or comparisons rather than education."
            )
        else:
            insights.append(
                "Viewer-intent driven content is limited, indicating an opportunity "
                "for more beginner-friendly or explanatory videos."
            )

    # -------- Topic-level insights --------
    if topic_gaps:
        gap_topics = [gap["topic"] for gap in topic_gaps if gap["count"] == 0]

        if gap_topics:
            insights.append(
                "The channel has almost no coverage on the following important topics: "
                + ", ".join(gap_topics) + "."
            )

        low_coverage_topics = [
            gap["topic"]
            for gap in topic_gaps
            if 0 < gap["count"] / total_videos < 0.2
        ]

        if low_coverage_topics:
            insights.append(
                "Some topics appear under-represented and could be expanded: "
                + ", ".join(low_coverage_topics) + "."
            )

    # -------- Strategic recommendations --------
    insights.append(
        "Content strategy recommendation: balance opinion-based videos "
        "with structured educational content to capture long-term audience trust."
    )

    return insights
