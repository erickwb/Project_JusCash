from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

model, feature_columns = joblib.load("../model_ml/XGBoost.pkl")

app = FastAPI()

class ProjectData(BaseModel):
    project_cost: float
    project_benefit: float
    roi: float
    year: int
    month: int

@app.post("/predict")
def predict(data: ProjectData):
    input_dict = {
        "Project Cost": data.project_cost,
        "Project Benefit": data.project_benefit,
        "ROI": data.roi,
        "Year": data.year,
        "Month": data.month
    }

    input_df = pd.DataFrame([input_dict])
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0.0
    input_df = input_df[feature_columns]

    prob = model.predict_proba(input_df)[0][1]
    pred = model.predict(input_df)[0]

    # Converter para tipos nativos do Python
    return {
        "success_probability": round(float(prob) * 100, 2),
        "prediction": "Sucesso" if int(pred) == 1 else "Fracasso"
    }
