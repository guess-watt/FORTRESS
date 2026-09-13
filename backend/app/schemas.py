from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    pgn: str = Field(..., min_length=1)


class AnalyzeResponse(BaseModel):
    anomaly_label: str
    isolation_score: float
    features: dict