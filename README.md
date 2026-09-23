# MachineMind — Predictive Maintenance & Machine Intelligence

An end-to-end machine learning system that predicts industrial machine failure from live sensor readings, logs every prediction to a database, and visualizes results on a real-time dashboard.

## Overview

Unplanned machine failure is expensive and disruptive. MachineMind demonstrates how a machine learning model can flag at-risk machinery *before* it fails, using sensor readings like temperature, rotational speed, torque, and tool wear. The system covers the full pipeline a real predictive maintenance product would need: data cleaning and feature engineering, model training and evaluation, a production-style API, a live dashboard, a persistent database, and a simulated IoT data stream.

## Key Features

- Trained binary classification model that predicts machine failure probability from 5 sensor readings and machine type
- REST API (FastAPI) that serves predictions in real time and returns a risk level (LOW / MEDIUM / HIGH) with a recommended action
- React dashboard for submitting readings and viewing prediction results
- Every prediction is logged to a SQLite database, with a "Recent Predictions" history view on the dashboard
- Simulated IoT sensor script that generates realistic readings and streams them through the same live pipeline
- Automated test suite (unit tests for feature engineering, integration tests for the API)

## Tech Stack

| Layer            | Technology                                  |
|-------------------|----------------------------------------------|
| Data & ML         | Python, Pandas, scikit-learn, joblib         |
| Backend API       | FastAPI, Uvicorn, Pydantic                   |
| Database          | SQLite                                       |
| Frontend          | React (Vite)                                 |
| Testing           | pytest, FastAPI TestClient                   |

## Architecture
Sensor Reading (real form input or simulated IoT script)
│
▼
FastAPI /predict endpoint
│
▼
Feature Engineering (Power, Temp Difference, Strain, Type encoding)
│
▼
Trained ML Pipeline (StandardScaler + Logistic Regression)
│
├──► Prediction + Risk Level + Recommended Action ──► React Dashboard
│
└──► Logged to SQLite (sensor_data + maintenance_records tables)
│
▼
GET /history endpoint ──► "Recent Predictions" table in React


## Dataset

This project uses the **AI4I 2020 Predictive Maintenance Dataset** (UCI Machine Learning Repository) — 10,000 rows of synthetic but realistic industrial sensor data, including air temperature, process temperature, rotational speed, torque, tool wear, and a machine failure label.

Five columns (`TWF`, `HDF`, `PWF`, `OSF`, `RNF`) were deliberately excluded from training. These columns are individual failure-mode flags that are direct components of the `Machine failure` target itself — including them would have caused data leakage, letting the model "cheat" by seeing pieces of the answer rather than learning from genuine sensor patterns.

## Machine Learning Approach

**Engineered features**, derived from the dataset's own documented failure-mechanism formulas:
- `Power [W]` = Torque × Rotational speed
- `Temp difference [K]` = Process temperature − Air temperature
- `Strain [Nm·min]` = Tool wear × Torque

**Handling class imbalance:** machine failures make up a small minority of the data (~3.5%). A naive model can reach ~97% accuracy just by always predicting "no failure" — while missing nearly every real failure. This project uses `class_weight="balanced"` in Logistic Regression (with `StandardScaler` for feature scaling) to explicitly penalize missed failures more heavily, trading some precision and overall accuracy for substantially higher recall on the failure class — the right tradeoff for predictive maintenance, where a missed failure is far more costly than an unnecessary inspection.

**Result:** ~86% overall accuracy with a substantially improved failure-detection recall compared to the unweighted baseline (see `notebooks/01_data_exploration.ipynb` for the full classification report and confusion matrix).

The trained pipeline (scaler + model) is saved with `joblib` alongside the exact feature column order it expects, so the API can reproduce identical preprocessing at inference time.

## Project Structure
machinemind/
├── data/ # Raw and processed datasets (not committed: machinemind.db)
├── models/ # Saved model pipeline and feature column list
├── notebooks/ # Data exploration, cleaning, training, evaluation
├── src/
│ ├── database.py # SQLite schema + logging + history queries
│ ├── features.py # Feature engineering logic (unit tested)
│ ├── simulate_iot.py # Simulated IoT sensor data generator
│ ├── test_features.py # Unit tests for feature engineering
│ ├── verify_db.py # Manual database sanity check
│ └── check_logs.py # Manual database sanity check
├── api/
│ ├── main.py # FastAPI app: /predict and /history endpoints
│ └── test_main.py # API integration tests
├── frontend/ # React (Vite) dashboard
└── requirements.txt


## Setup & Installation

### 1. Clone and set up the Python environment
git clone https://github.com/Sachinbs13/Machinemind.git
cd machinemind
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

### 2. Initialize the database
cd src
python database.py


### 3. Run the backend API
cd api
uvicorn main:app --reload --port 8001
API docs available at `http://127.0.0.1:8001/docs`

### 4. Run the frontend
cd frontend
npm install
npm run dev
Dashboard available at `http://localhost:5173`

### 5. (Optional) Run the simulated IoT sensor stream
cd src
python simulate_iot.py

## API Reference

**POST /predict** — submit a sensor reading, get a prediction

Request body:
```json
{
  "machine_id": "M001",
  "air_temperature": 300.0,
  "process_temperature": 310.0,
  "rotational_speed": 1500.0,
  "torque": 40.0,
  "tool_wear": 10.0,
  "type": "M"
}
```

Response:
```json
{
  "machine_id": "M001",
  "prediction": 0,
  "risk_level": "LOW",
  "probability": 0.0092,
  "recommended_action": "No action needed. Continue normal operation."
}
```

**GET /history?limit=20** — most recent logged predictions, newest first

## Testing
cd src
pytest -v

cd ../api
pytest -v

## Future Improvements

- Compare Logistic Regression against tree-based models (Decision Tree, Random Forest) for accuracy/recall tradeoffs
- Add authentication to the API
- Containerize with Docker and deploy to a cloud provider
- Add sensor trend charts (time-series view of a machine's readings over time)
- Automatic model retraining pipeline as new logged data accumulates

## Author

Built by Sachin as a hands-on predictive maintenance / ML systems project, covering the full path from raw data to a working, tested, deployed-style application.
