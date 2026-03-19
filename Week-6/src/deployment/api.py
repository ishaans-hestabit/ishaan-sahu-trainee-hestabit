import uuid
import json
import pickle
import csv
import os
from datetime import datetime
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("models/best_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("features/feature_list.json") as f:
    FEATURES = json.load(f)["selected_features"]

app = FastAPI(title="MBA Placement Prediction API")

class PredictRequest(BaseModel):
    features: dict

class PredictResponse(BaseModel):
    request_id : str
    prediction : int
    label      : str
    probability: float
    timestamp  : str

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):

    X_raw   = np.array([[request.features.get(f, 0) for f in FEATURES]])
    X       = scaler.transform(X_raw)

    prediction  = int(model.predict(X)[0])
    probability = float(model.predict_proba(X)[0][1])
    request_id  = str(uuid.uuid4())
    timestamp   = datetime.utcnow().isoformat()

    log_exists = os.path.exists("prediction_logs.csv")
    with open("prediction_logs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow(["request_id", "timestamp", "prediction", "probability"] + FEATURES)
        writer.writerow([request_id, timestamp, prediction, round(probability, 4)]
                        + [request.features.get(f, 0) for f in FEATURES])

    return PredictResponse(
        request_id  = request_id,
        prediction  = prediction,
        label       = "Placed" if prediction == 1 else "Not Placed",
        probability = round(probability, 4),
        timestamp   = timestamp
    )

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}