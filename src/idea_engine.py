from src.domain_detection import extract_domain_topics

def is_person_name(keyword: str) -> bool:
    words = keyword.strip().split()
    return len(words) <= 3

DOMAIN_TOPICS = [
    "personal finance",
    "mutual funds",
    "salary planning",
    "money management",
    "career growth",
    "investing",
    "middle class finance"
]


def generate_video_ideas(keyword: str, gaps: list, videos: list):
    ideas = []

    topics = extract_domain_topics(videos)

    if not topics:
        topics = [keyword]

    TEMPLATES = [
        "Why Most People Get {topic} Wrong ({intent} Explained)",
        "{intent_cap} in {topic}: What No One Tells Beginners",
        "Before You Start {topic}: The {intent} You Must Know",
        "{topic} for Beginners – {intent_cap} That People Miss",
        "The Real {intent} About {topic} (Not Clickbait)",
        "{intent_cap} Mistakes in {topic} Everyone Makes",
    ]

    for gap in gaps:
        intent = gap["intent"]
        intent_cap = intent.capitalize()

        for topic in topics:
            for template in TEMPLATES:
                ideas.append(
                    template.format(
                        topic=topic.title(),
                        intent=intent,
                        intent_cap=intent_cap
                    )
                )

    return ideas
