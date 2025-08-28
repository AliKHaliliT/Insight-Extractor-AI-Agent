from enum import Enum


class InsightType(str, Enum):
    QUANTITATIVE_METRIC = "Quantitative Metric"
    KEY_THEME = "Key Theme"
    SENTIMENT_ANALYSIS = "Sentiment Analysis"
    TABLE_ANALYSIS = "Table Analysis"
    CODE_ANALYSIS = "Code Analysis"