from typing import Annotated, Literal, Optional

from pydantic import StringConstraints

from .base_insight import BaseInsight
from .taxonomy.insight_type import InsightType


class CodeInsight(BaseInsight):
    insight_type: Literal[InsightType.CODE_ANALYSIS] = InsightType.CODE_ANALYSIS
    language: Annotated[str, StringConstraints(min_length=1)]
    summary: Annotated[str, StringConstraints(min_length=20)]
    potential_issues: Optional[list[str]] = None