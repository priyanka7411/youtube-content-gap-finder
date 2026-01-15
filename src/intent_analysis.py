import re
from collections import Counter

INTENT_WORDS = {
    "why",
    "mistake", "mistakes",
    "beginner", "beginners",
    "avoid",
    "scam",
    "truth",
    "vs",
    "difference",
    "problem", "problems",
    "risk",
    "myth", "myths",
    "hidden"
}

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_intent_counts(videos: list) -> dict:
    """
    Takes list of video dicts and returns intent frequency.
    """

    hits = []

    for video in videos:
        combined_text = clean_text(
            video["title"] + " " + video["description"]
        )

        for intent in INTENT_WORDS:
            if intent in combined_text:
                hits.append(intent)

    return dict(Counter(hits))
