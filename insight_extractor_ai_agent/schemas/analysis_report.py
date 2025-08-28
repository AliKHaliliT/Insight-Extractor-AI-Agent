from datetime import datetime, timezone
from typing import Annotated, Union

from pydantic import BaseModel, Field, StringConstraints

from .code_insight import CodeInsight
from .quantitative_insight import QuantitativeInsight
from .sentiment_insight import SentimentInsight
from .table_insight import TableInsight
from .thematic_insight import ThematicInsight


class AnalysisReport(BaseModel):
    file_name: str
    file_type_detected: str
    analysis_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_used: str
    executive_summary: Annotated[str, StringConstraints(min_length=20)]
    insights: list[Union[QuantitativeInsight, ThematicInsight, SentimentInsight, TableInsight, CodeInsight]] = Field(..., min_length=1)