from typing import Annotated, Literal, Optional

from pydantic import StringConstraints

from .base_insight import BaseInsight
from .taxonomy.insight_type import InsightType


class TableInsight(BaseInsight):
    insight_type: Literal[InsightType.TABLE_ANALYSIS] = InsightType.TABLE_ANALYSIS
    summary: Annotated[str, StringConstraints(min_length=20)]
    table_headers: Optional[list[str]] = None