import streamlit as st

from src.youtube_api import fetch_videos, fetch_channel_videos
from src.intent_analysis import extract_intent_counts
from src.gap_analysis import identify_content_gaps
from src.idea_engine import generate_video_ideas
from src.topic_clustering import cluster_topics
from src.topic_gap_analysis import identify_topic_gaps
from src.strategy_summary import generate_strategy_summary


# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="YouTube Content Gap Finder",
    layout="centered"
)

st.title("🎥 YouTube Content Gap Finder")
st.write("Identify content gaps and strategic opportunities on YouTube.")

st.markdown("""
This tool helps creators, marketers, and researchers understand  
**what content is missing** in a niche or on a specific YouTube channel.

It focuses on:
- viewer intent (why, mistakes, beginner, etc.)
- topic coverage and blind spots
- high-level content strategy insights

It does **not** generate final YouTube titles.
Use the results as **direction**, not copy-paste output.
""")

# -------------------------------------------------
# Mode selector (V3.5 core UX)
# -------------------------------------------------
analysis_mode = st.radio(
    "Choose analysis type",
    ["Keyword-based analysis", "Channel-based analysis"]
)

st.divider()

# =================================================
# MODE 1 — KEYWORD ANALYSIS (V1)
# =================================================
if analysis_mode == "Keyword-based analysis":

    keyword = st.text_input(
        "Enter a YouTube keyword or niche",
        placeholder="e.g. data science tutorials, dance class"
    )

    max_results = st.slider(
        "Number of videos to analyze",
        min_value=5,
        max_value=50,
        value=20,
        step=5
    )

    if st.button("Run Keyword Analysis"):

        if not keyword.strip():
            st.warning("Please enter a keyword.")
            st.stop()

        with st.spinner("Analyzing YouTube videos..."):
            videos = fetch_videos(keyword, max_results=max_results)

        if not videos:
            st.warning(
                "⚠️ Unable to fetch YouTube data right now.\n\n"
                "This may be due to API limits.\n"
                "Try a smaller or more specific keyword."
            )
            st.stop()

        intent_counts = extract_intent_counts(videos)

        st.success(f"Analyzed {len(videos)} videos")

        # -------- Existing Videos --------
        st.subheader("📌 Sample Videos Found")
        for i, video in enumerate(videos[:10], start=1):
            st.markdown(f"**{i}. {video['title']}**")
            st.caption(f"Channel: {video['channel']}")

        # -------- Viewer Intent --------
        st.divider()
        st.subheader("🧠 Viewer Intent Detected")

        if intent_counts:
            for intent, count in sorted(intent_counts.items(), key=lambda x: -x[1]):
                st.write(f"**{intent}** → {count} videos")
        else:
            st.info("No strong viewer intent signals detected.")

        # -------- Content Gaps --------
        st.divider()
        st.subheader("🚨 Content Gaps")

        gaps = identify_content_gaps(
            intent_counts=intent_counts,
            total_videos=len(videos)
        )

        if gaps:
            for gap in gaps:
                st.write(
                    f"**{gap['intent']}** → "
                    f"{gap['count']} videos "
                    f"({gap['ratio']*100:.0f}% coverage)"
                )
        else:
            st.info("No major content gaps found.")

        # -------- Content Angles --------
        st.divider()
        st.subheader("💡 Content Angles to Explore")

        ideas = generate_video_ideas(keyword, gaps, videos)

        for idea in ideas[:10]:
            st.markdown(f"- {idea}")

# =================================================
# MODE 2 — CHANNEL ANALYSIS (V3)
# =================================================
else:

    channel_url = st.text_input(
        "Enter a YouTube channel URL",
        placeholder="e.g. https://www.youtube.com/@warikoo"
    )

    max_results = st.slider(
        "Number of channel videos to analyze",
        min_value=5,
        max_value=50,
        value=20,
        step=5
    )

    if st.button("Run Channel Analysis"):

        if not channel_url.strip():
            st.warning("Please enter a channel URL.")
            st.stop()

        with st.spinner("Analyzing channel content..."):
            videos = fetch_channel_videos(channel_url, max_results=max_results)

        if not videos:
            st.warning(
                "⚠️ Unable to fetch channel data.\n\n"
                "Please check the channel URL or try again later."
            )
            st.stop()

        intent_counts = extract_intent_counts(videos)
        topic_counts = cluster_topics(videos)
        topic_gaps = identify_topic_gaps(
            topic_counts,
            total_videos=len(videos)
        )

        st.success(f"Analyzed {len(videos)} channel videos")

        # -------- Viewer Intent --------
        st.subheader("🧠 Viewer Intent Coverage")

        if intent_counts:
            for intent, count in intent_counts.items():
                st.write(f"**{intent}** → {count} videos")
        else:
            st.info("Very little explicit viewer-intent driven content detected.")

        # -------- Topic Coverage --------
        st.divider()
        st.subheader("🧩 Topic Coverage")

        for topic, count in topic_counts.items():
            st.write(f"**{topic}** → {count} videos")

        # -------- Topic Gaps --------
        st.divider()
        st.subheader("🚨 Topic Gaps")

        if topic_gaps:
            for gap in topic_gaps:
                st.write(
                    f"**{gap['topic']}** → "
                    f"{gap['count']} videos "
                    f"({gap['coverage']*100:.0f}% coverage)"
                )
        else:
            st.info("No major topic gaps identified.")

        # -------- Strategy Summary --------
        st.divider()
        st.subheader("📊 Channel Strategy Summary")

        summary = generate_strategy_summary(
            intent_counts=intent_counts,
            topic_counts=topic_counts,
            topic_gaps=topic_gaps,
            total_videos=len(videos)
        )

        for line in summary:
            st.markdown(f"- {line}")
