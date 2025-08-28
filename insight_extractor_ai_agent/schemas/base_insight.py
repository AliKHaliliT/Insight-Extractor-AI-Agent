from typing import Annotated, Optional

from pydantic import BaseModel, Field, StringConstraints

from .location_reference import LocationReference
from .taxonomy.insight_type import InsightType
from .taxonomy.severity_level import SeverityLevel


class BaseInsight(BaseModel):
    title: Annotated[str, StringConstraints(min_length=5, max_length=150)]
    description: Annotated[str, StringConstraints(min_length=10)]
    insight_type: InsightType
    severity: SeverityLevel
    confidence_score: Annotated[float, Field(ge=0.0, le=1.0)]
    locations: list[LocationReference] = Field(..., min_length=1)
    representative_snippet: Optional[Annotated[str, StringConstraints(min_length=10)]] = None
    actionable_recommendation: Optional[Annotated[str, StringConstraints(min_length=10)]] = None