import streamlit as st
from src.youtube_api import fetch_videos
from src.intent_analysis import extract_intent_counts
from src.gap_analysis import identify_content_gaps
from src.idea_engine import generate_video_ideas
from src.topic_clustering import cluster_topics
from src.topic_gap_analysis import identify_topic_gaps
from data.sample_videos_v2 import sample_videos



st.set_page_config(page_title="YouTube Content Gap Finder", layout="centered")

st.title("🎥 YouTube Content Gap Finder")
st.write("Find content gaps based on viewer intent")

st.markdown("""
### How to use this tool (V1)

This tool analyzes a YouTube **niche or keyword** to find  
**under-covered viewer intents** like *why*, *mistakes*, *avoid*, *beginner*.

It does **not** generate final YouTube titles.

Instead, it helps you:
- understand what angles are missing in your niche
- decide **what kind of content to create next**
- avoid guessing blindly

Use the results below as **direction**, not copy-paste titles.
""")


keyword = st.text_input(
    "Enter a YouTube keyword or niche",
    placeholder="e.g. dance class, data science tutorials"
)

max_results = st.slider(
    "Number of videos to analyze",
    min_value=5,
    max_value=50,
    value=20,
    step=5
)

if st.button("Analyze Niche"):

    if not keyword.strip():
        st.warning("Please enter a keyword.")
        st.stop()

    with st.spinner("Analyzing YouTube videos..."):
        videos = fetch_videos(keyword, max_results=max_results)

    # ✅ Graceful failure handling (V1)
    if not videos:
        st.warning(
            "⚠️ Unable to fetch YouTube data right now.\n\n"
            "This may be due to API limits or temporary restrictions.\n"
            "Try a smaller or more specific keyword."
        )
        st.stop()

    intent_counts = extract_intent_counts(videos)

    st.success(f"Analyzed {len(videos)} videos")

    # ---------------- Existing Videos ----------------
    st.subheader("📌 Existing Videos")
    for i, video in enumerate(videos[:10], start=1):
        st.markdown(f"**{i}. {video['title']}**")
        st.caption(f"Channel: {video['channel']}")

    # ---------------- Viewer Intent ----------------
    st.divider()
    st.subheader("🧠 Viewer Intent Found")

    if intent_counts:
        for intent, count in sorted(intent_counts.items(), key=lambda x: -x[1]):
            st.write(f"**{intent}** → {count} videos")
    else:
        st.info("No strong intent signals found.")

    # ---------------- Content Gaps ----------------
    st.divider()
    st.subheader("🚨 Content Gaps Identified")

    gaps = identify_content_gaps(
        intent_counts=intent_counts,
        total_videos=len(videos)
    )

    if gaps:
        for gap in gaps:
            st.write(
                f"**{gap['intent']}** → {gap['count']} videos "
                f"({gap['ratio']*100:.0f}% coverage)"
            )
    else:
        st.info("No major content gaps found.")

    # ---------------- Content Angles ----------------
    st.divider()
    st.subheader("💡 Content Angles You Can Explore")

    ideas = generate_video_ideas(keyword, gaps, videos)

    for idea in ideas[:10]:
        st.markdown(f"- {idea}")
        
        # =======================
    
    # V2: Topic Gap Analysis
    # =======================

    st.divider()
    st.subheader("🧩 V2 – Topic Coverage & Gaps")

    # Use cached/sample data for V2
    topic_counts = cluster_topics(sample_videos)
    topic_gaps = identify_topic_gaps(
        topic_counts,
        total_videos=len(sample_videos)
    )

    st.markdown("**Topic Coverage:**")
    for topic, count in topic_counts.items():
        st.write(f"- {topic}: {count} videos")

    st.markdown("**Under-covered Topics (Gaps):**")
    if topic_gaps:
        for gap in topic_gaps:
            st.write(
                f"• **{gap['topic']}** → "
                f"{gap['count']} videos "
                f"({gap['coverage']*100:.0f}% coverage)"
            )
    else:
        st.info("No major topic gaps identified.")
