from .base_insight import BaseInsight
from typing import Literal, Annotated, Union, Optional
from .taxonomy.insight_type import InsightType
from pydantic import StringConstraints


class QuantitativeInsight(BaseInsight):
    insight_type: Literal[InsightType.QUANTITATIVE_METRIC] = InsightType.QUANTITATIVE_METRIC
    metric_name: Annotated[str, StringConstraints(min_length=3)]
    value: Union[float, int]
    unit: Optional[str] = None