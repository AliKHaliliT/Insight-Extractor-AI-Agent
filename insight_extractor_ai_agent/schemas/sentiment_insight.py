from typing import Literal

from .base_insight import BaseInsight
from .sentiment_result import SentimentResult
from .taxonomy.insight_type import InsightType


class SentimentInsight(BaseInsight):
    insight_type: Literal[InsightType.SENTIMENT_ANALYSIS] = InsightType.SENTIMENT_ANALYSIS
    sentiment: SentimentResult