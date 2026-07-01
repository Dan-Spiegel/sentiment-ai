from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

from app.sentiment import analyze_sentiment

app = FastAPI(title="SentimentAI", version="1.0.0")

# expose /metrics pour Prometheus
Instrumentator().instrument(app).expose(app)


class TextIn(BaseModel):
    text: str


class SentimentOut(BaseModel):
    text: str
    sentiment: str
    score: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=SentimentOut)
def predict(payload: TextIn):
    label, score = analyze_sentiment(payload.text)
    return SentimentOut(text=payload.text, sentiment=label, score=score)
