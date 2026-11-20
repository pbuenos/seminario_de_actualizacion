from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


MODEL_PATH = Path(__file__).resolve().parents[1] / "modelo" / "modelo.joblib"


class EntradaEmpleado(BaseModel):
    edad: int = Field(ge=18, le=75)
    departamento: Literal[
        "Sales",
        "Research & Development",
        "Human Resources",
    ]
    rol: Literal[
        "Healthcare Representative",
        "Laboratory Technician",
        "Manager",
        "Manufacturing Director",
        "Research Director",
        "Research Scientist",
        "Sales Executive",
        "Sales Representative",
        "Human Resources",
    ]
    salario_mensual: float = Field(ge=0)
    satisfaccion_laboral: int = Field(ge=1, le=4)
    anos_en_la_empresa: int = Field(ge=0)
    horas_extras: Literal["Yes", "No"]
    distancia_al_hogar: int = Field(ge=1)
    equilibrio_vida_trabajo: int = Field(ge=1, le=4)
    anos_desde_ultimo_ascenso: int = Field(ge=0)


app = FastAPI(
    title="API de riesgo de abandono",
    description="Predice el riesgo de abandono laboral con un modelo propio.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

modelo_payload = joblib.load(MODEL_PATH)
modelo = modelo_payload["model"]
feature_names = modelo_payload["feature_names"]
ENTRADA_A_DATASET = {
    "Age": "edad",
    "Department": "departamento",
    "JobRole": "rol",
    "MonthlyIncome": "salario_mensual",
    "JobSatisfaction": "satisfaccion_laboral",
    "YearsAtCompany": "anos_en_la_empresa",
    "OverTime": "horas_extras",
    "DistanceFromHome": "distancia_al_hogar",
    "WorkLifeBalance": "equilibrio_vida_trabajo",
    "YearsSinceLastPromotion": "anos_desde_ultimo_ascenso",
}


@app.get("/health")
def health():
    return {
        "estado": "ok",
        "modelo": modelo_payload.get("model_name", "modelo"),
        "scikit_learn": modelo_payload["sklearn_version"],
        "dataset": modelo_payload["dataset_name"],
    }


@app.post("/predecir")
def predecir(datos: EntradaEmpleado):
    fila = pd.DataFrame(
        [
            {
                campo_dataset: getattr(datos, campo_api)
                for campo_dataset, campo_api in ENTRADA_A_DATASET.items()
                if campo_dataset in feature_names
            }
        ],
        columns=feature_names,
    )
    probabilidad_abandono = float(modelo.predict_proba(fila)[0][1])
    prediccion = int(probabilidad_abandono >= 0.5)

    if probabilidad_abandono >= 0.70:
        riesgo = "Alto"
    elif probabilidad_abandono >= 0.45:
        riesgo = "Medio"
    else:
        riesgo = "Bajo"

    return {
        "prediccion": "Probable abandono" if prediccion else "Probable permanencia",
        "probabilidad": round(probabilidad_abandono, 4),
        "riesgo": riesgo,
    }


frontend_path = Path(__file__).resolve().parents[1] / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
