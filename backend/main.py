from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from models.poutmodels import EmailOut 
from models.pinmodels import EmailIn
import tensorflow as tf
import numpy as np


CLASSES = ["spam", "work", "school", "social", "advertisement", "news"]
CLASS_TO_ID = {c: i for i, c in enumerate(CLASSES)}
ID_TO_CLASS = {i: c for c, i in CLASS_TO_ID.items()}  # same as dict(enumerate(CLASSES))


def load_model_file(model_path: str) -> tf.keras.Model:
    """Wrapper to load a Keras model with a clean error message."""
    try:
        return tf.keras.models.load_model(model_path)
    except Exception as e:
        raise IOError(f"Failed to load model from {model_path}. Error: {e}") from e


def predict(model: tf.keras.Model, texts: list[str] | str) -> list[dict]:
    """
    texts: list[str] or str
    returns: list of dicts with class + probabilities
    """
    if isinstance(texts, str):
        texts = [texts]

    # Convert to tf.constant immediately to avoid dtype issues
    input_tensor = tf.constant(texts)

    probs = model.predict(input_tensor, verbose=0)

    # Sanity check: model output dimension should match number of classes
    # (only checks first row)
    if len(probs) > 0 and probs.shape[-1] != len(CLASSES):
        raise ValueError(
            f"Model output has {probs.shape[-1]} classes, but CLASSES has {len(CLASSES)}. "
            "Your CLASSES ordering/list may not match the trained model."
        )

    results = []
    for p in probs:
        pred_id = int(np.argmax(p))
        results.append({
            "pred": ID_TO_CLASS[pred_id],
            "confidence": float(p[pred_id]),
            "all_probs": {ID_TO_CLASS[i]: float(p[i]) for i in range(len(CLASSES))},
        })
    return results


MODEL_PATH = "model.keras"

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = None
    try:
        app.state.model = load_model_file(MODEL_PATH)
        print(f"Model loaded: {MODEL_PATH}")
        yield
    finally:
        if getattr(app.state, "model", None) is not None:
            del app.state.model
        print("Shutdown complete")


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/api/email", response_model=EmailOut)
def classify_email(email: EmailIn):
    model = getattr(app.state, "model", None)
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
        
    text = email.body.strip()
    text = text.replace('\n', '').replace('\r', '').replace('\t','')

    try:
        res = predict(model, text)[0]
        return res  # matches EmailOut keys
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

