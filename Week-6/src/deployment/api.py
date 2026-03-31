import uuid
import json
import pickle
import csv
import os
from datetime import datetime
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from features.build_features import generate_features  

with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("models/best_model_prod.pkl", "rb") as f:
    model = pickle.load(f)

with open("features/feature_list.json") as f:
    FEATURES = json.load(f)["selected_features"]

app = FastAPI(title="MBA Placement Prediction API")

class PredictRequest(BaseModel):
    gender        : str
    ssc_p         : float
    ssc_b         : str
    hsc_p         : float
    hsc_b         : str
    hsc_s         : str
    degree_p      : float
    degree_t      : str
    workex        : str
    etest_p       : float
    specialisation: str
    mba_p         : float

class PredictResponse(BaseModel):
    request_id : str
    prediction : int
    label      : str
    probability: float
    timestamp  : str

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):

    # step 1 — raw input into dataframe
    df = pd.DataFrame([request.model_dump()])

    # step 2 — same function used during training
    df = generate_features(df)

    # step 3 — encode categoricals same way as training
    cat_cols = df.select_dtypes(include=["object", 'string']).columns
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    # step 4 — align to exact 20 features model expects
    df = df.reindex(columns=FEATURES, fill_value=0)

    # step 5 — scale and predict
    X = scaler.transform(df.values)

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
                        + df.values[0].tolist())

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