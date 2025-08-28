from typing import Annotated, Literal, Optional, Union

from pydantic import StringConstraints

from .base_insight import BaseInsight
from .taxonomy.insight_type import InsightType


class QuantitativeInsight(BaseInsight):
    insight_type: Literal[InsightType.QUANTITATIVE_METRIC] = InsightType.QUANTITATIVE_METRIC
    metric_name: Annotated[str, StringConstraints(min_length=3)]
    value: Union[float, int]
    unit: Optional[str] = None