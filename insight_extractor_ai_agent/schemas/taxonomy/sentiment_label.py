from enum import Enum


class SentimentLabel(str, Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"
    MIXED = "Mixed"