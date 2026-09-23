import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

from database import log_prediction, get_recent_predictions
from features import engineer_features

app = FastAPI(title="MachineMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = joblib.load("../models/machine_failure_model.pkl")
feature_columns = joblib.load("../models/feature_columns.pkl")

class SensorInput(BaseModel):
    machine_id: str
    air_temperature: float
    process_temperature: float
    rotational_speed: float
    torque: float
    tool_wear: float
    type: str  # "L", "M", or "H"

@app.post("/predict")
def predict(data: SensorInput):
    row = engineer_features(
        air_temperature=data.air_temperature,
        process_temperature=data.process_temperature,
        rotational_speed=data.rotational_speed,
        torque=data.torque,
        tool_wear=data.tool_wear,
        machine_type=data.type,
    )

    input_df = pd.DataFrame([row])
    input_df = input_df.reindex(columns=feature_columns, fill_value=0)

    prediction = pipeline.predict(input_df)[0]
    probability = pipeline.predict_proba(input_df)[0][1]

    if probability >= 0.6:
        risk_level = "HIGH"
        recommended_action = "Schedule maintenance inspection immediately."
    elif probability >= 0.3:
        risk_level = "MEDIUM"
        recommended_action = "Monitor closely; consider a routine inspection."
    else:
        risk_level = "LOW"
        recommended_action = "No action needed. Continue normal operation."

    log_prediction(
        machine_id=data.machine_id,
        machine_type=data.type,
        air_temperature=data.air_temperature,
        process_temperature=data.process_temperature,
        rotational_speed=data.rotational_speed,
        torque=data.torque,
        tool_wear=data.tool_wear,
        predicted_failure=int(prediction),
        risk_level=risk_level,
        probability=round(float(probability), 4),
        recommended_action=recommended_action,
    )

    return {
        "machine_id": data.machine_id,
        "prediction": int(prediction),
        "risk_level": risk_level,
        "probability": round(float(probability), 4),
        "recommended_action": recommended_action,
    }

@app.get("/history")
def get_history(limit: int = 20):
    records = get_recent_predictions(limit)
    return {"records": records}