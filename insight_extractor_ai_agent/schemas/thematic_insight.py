from typing import Literal

from pydantic import Field, PositiveInt

from .base_insight import BaseInsight
from .taxonomy.insight_type import InsightType


class ThematicInsight(BaseInsight):
    insight_type: Literal[InsightType.KEY_THEME] = InsightType.KEY_THEME
    keywords: list[str] = Field(..., min_length=1)
    mentions: PositiveInt