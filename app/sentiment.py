# analyse de sentiment simple basee sur deux listes de mots

POSITIVE_WORDS = {
    "good", "great", "excellent", "love", "wonderful", "amazing",
    "happy", "fantastic", "awesome", "nice", "best", "perfect",
}
NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "hate", "horrible", "worst",
    "sad", "poor", "disappointing", "ugly", "boring", "broken",
}


def analyze_sentiment(text):
    tokens = [t.strip(".,!?;:").lower() for t in text.split()]
    pos = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg = sum(1 for t in tokens if t in NEGATIVE_WORDS)
    total = pos + neg
    if total == 0:
        return "neutral", 0.0
    score = (pos - neg) / total
    if score > 0:
        return "positive", round(score, 3)
    if score < 0:
        return "negative", round(score, 3)
    return "neutral", 0.0
