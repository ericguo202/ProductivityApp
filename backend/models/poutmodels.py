from pydantic import BaseModel

class EmailOut(BaseModel):
    pred: str
    confidence: float
    all_probs: dict[str, float]

