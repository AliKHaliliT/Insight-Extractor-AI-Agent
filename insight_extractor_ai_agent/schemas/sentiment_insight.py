from .base_insight import BaseInsight
from typing import Literal
from .taxonomy.insight_type import InsightType
from .sentiment_result import SentimentResult


class SentimentInsight(BaseInsight):
    insight_type: Literal[InsightType.SENTIMENT_ANALYSIS] = InsightType.SENTIMENT_ANALYSIS
    sentiment: SentimentResult