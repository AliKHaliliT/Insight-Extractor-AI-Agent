from .base_insight import BaseInsight
from typing import Literal, Annotated, Optional
from .taxonomy.insight_type import InsightType
from pydantic import StringConstraints


class TableInsight(BaseInsight):
    insight_type: Literal[InsightType.TABLE_ANALYSIS] = InsightType.TABLE_ANALYSIS
    summary: Annotated[str, StringConstraints(min_length=20)]
    table_headers: Optional[list[str]] = None