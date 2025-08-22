from .base_insight import BaseInsight
from typing import Literal, Annotated, Optional
from .taxonomy.insight_type import InsightType
from pydantic import StringConstraints


class CodeInsight(BaseInsight):
    insight_type: Literal[InsightType.CODE_ANALYSIS] = InsightType.CODE_ANALYSIS
    language: Annotated[str, StringConstraints(min_length=1)]
    summary: Annotated[str, StringConstraints(min_length=20)]
    potential_issues: Optional[list[str]] = None