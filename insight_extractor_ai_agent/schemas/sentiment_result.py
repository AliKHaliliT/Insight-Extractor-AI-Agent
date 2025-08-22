from pydantic import BaseModel, Field, StringConstraints
from .taxonomy.sentiment_label import SentimentLabel
from typing import Annotated



class SentimentResult(BaseModel):
    label: SentimentLabel
    score: Annotated[float, Field(ge=-1.0, le=1.0)]
    explanation: Annotated[str, StringConstraints(min_length=10)]