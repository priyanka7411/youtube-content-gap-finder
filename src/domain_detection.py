import re
from collections import Counter

STOPWORDS = {
    "the","and","to","of","in","for","on","with","a","is","this","that",
    "shorts","short","video","vlog","episode","ep","new"
}

def clean_text(text: str) -> list:
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return [
        w for w in text.split()
        if w not in STOPWORDS and len(w) > 3
    ]


def extract_domain_topics(videos: list, top_n: int = 5) -> list:
    words = []

    for video in videos:
        words.extend(clean_text(video["title"]))

    common = Counter(words).most_common(top_n)
    return [w for w, _ in common]
