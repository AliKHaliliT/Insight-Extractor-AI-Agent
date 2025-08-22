from .base_insight import BaseInsight
from typing import Literal
from .taxonomy.insight_type import InsightType
from pydantic import Field, PositiveInt


class ThematicInsight(BaseInsight):
    insight_type: Literal[InsightType.KEY_THEME] = InsightType.KEY_THEME
    keywords: list[str] = Field(..., min_length=1)
    mentions: PositiveInt