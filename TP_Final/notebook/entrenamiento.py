"""Entrena y exporta el modelo a partir del dataset IBM HR de demostracion."""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
MODEL_PATH = ROOT / "app" / "modelo" / "modelo.joblib"
RANDOM_SEED = 42
FEATURES = [
    "Age",
    "Department",
    "JobRole",
    "MonthlyIncome",
    "JobSatisfaction",
    "YearsAtCompany",
    "OverTime",
    "DistanceFromHome",
    "WorkLifeBalance",
    "YearsSinceLastPromotion",
]
TARGET = "Attrition"


def entrenar() -> dict:
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"No se encontro el dataset: {DATA_PATH}")

    datos = pd.read_csv(DATA_PATH)
    columnas_requeridas = FEATURES + [TARGET]
    faltantes = [columna for columna in columnas_requeridas if columna not in datos]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas en el CSV: {faltantes}")
    if datos[columnas_requeridas].isna().any().any():
        raise ValueError("El dataset tiene valores faltantes en columnas utilizadas.")

    etiquetas_desconocidas = set(datos[TARGET].unique()) - {"Yes", "No"}
    if etiquetas_desconocidas:
        raise ValueError(
            f"Etiquetas inesperadas en {TARGET}: {sorted(etiquetas_desconocidas)}"
        )

    X = datos[FEATURES]
    y = datos[TARGET].map({"No": 0, "Yes": 1})

    X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_SEED,
        stratify=y,
    )

    categoricas = ["Department", "JobRole", "OverTime"]
    numericas = [columna for columna in FEATURES if columna not in categoricas]

    preprocesamiento = ColumnTransformer(
        [
            ("numericas", StandardScaler(), numericas),
            ("categoricas", OneHotEncoder(handle_unknown="ignore"), categoricas),
        ]
    )
    candidatos = {
        "regresion_logistica": Pipeline(
            [
                ("preprocesamiento", preprocesamiento),
                (
                    "clasificador",
                    LogisticRegression(
                        max_iter=1000,
                        class_weight="balanced",
                        random_state=RANDOM_SEED,
                    ),
                ),
            ]
        ),
        "random_forest": Pipeline(
            [
                ("preprocesamiento", preprocesamiento),
                (
                    "clasificador",
                    RandomForestClassifier(
                        n_estimators=200,
                        max_depth=10,
                        min_samples_leaf=3,
                        class_weight="balanced",
                        random_state=RANDOM_SEED,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
    }

    particiones = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_SEED,
    )
    resultados = {}
    for nombre, candidato in candidatos.items():
        puntajes_cv = cross_val_score(
            candidato,
            X_entrenamiento,
            y_entrenamiento,
            cv=particiones,
            scoring="f1",
        )
        resultados[nombre] = {
            "modelo": candidato,
            "f1_validacion_cruzada": float(puntajes_cv.mean()),
            "desviacion_f1_validacion_cruzada": float(puntajes_cv.std()),
        }

    modelo_nombre = max(
        resultados,
        key=lambda nombre: resultados[nombre]["f1_validacion_cruzada"],
    )
    modelo = resultados[modelo_nombre]["modelo"]
    modelo.fit(X_entrenamiento, y_entrenamiento)
    predicciones = modelo.predict(X_prueba)
    probabilidades = modelo.predict_proba(X_prueba)[:, 1]
    metricas = {
        "accuracy": accuracy_score(y_prueba, predicciones),
        "precision": precision_score(y_prueba, predicciones, zero_division=0),
        "recall": recall_score(y_prueba, predicciones, zero_division=0),
        "f1": f1_score(y_prueba, predicciones, zero_division=0),
        "roc_auc": roc_auc_score(y_prueba, probabilidades),
        "f1_validacion_cruzada": resultados[modelo_nombre][
            "f1_validacion_cruzada"
        ],
        "desviacion_f1_validacion_cruzada": resultados[modelo_nombre][
            "desviacion_f1_validacion_cruzada"
        ],
        "matriz_confusion": confusion_matrix(y_prueba, predicciones).tolist(),
        "reporte": classification_report(y_prueba, predicciones),
        "modelo_seleccionado": modelo_nombre,
        "comparacion_modelos": {
            nombre: {
                "f1_validacion_cruzada": round(
                    resultado["f1_validacion_cruzada"], 4
                ),
                "desviacion": round(
                    resultado["desviacion_f1_validacion_cruzada"], 4
                ),
            }
            for nombre, resultado in resultados.items()
        },
    }

    payload = {
        "model": modelo,
        "feature_names": FEATURES,
        "categorical_features": categoricas,
        "sklearn_version": sklearn.__version__,
        "model_name": modelo_nombre,
        "dataset_name": DATA_PATH.name,
        "training_rows": len(datos),
        "target_counts": y.value_counts().sort_index().to_dict(),
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, MODEL_PATH)

    print(f"Dataset: {DATA_PATH.name} ({len(datos)} filas, {len(datos.columns)} columnas)")
    print(f"Distribucion objetivo: {y.value_counts().sort_index().to_dict()} (0=No, 1=Yes)")
    print("Division: 80% entrenamiento / 20% prueba")
    print("Seleccion de modelo usando solo entrenamiento, CV estratificada de 5 folds:")
    for nombre, metricas_candidato in metricas["comparacion_modelos"].items():
        print(f"  {nombre}: {metricas_candidato}")
    print(f"Modelo seleccionado por F1 CV: {modelo_nombre}")
    for nombre in (
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "f1_validacion_cruzada",
    ):
        print(f"{nombre}: {metricas[nombre]:.4f}")
    print("Matriz de confusion:")
    print(np.array(metricas["matriz_confusion"]))
    print(metricas["reporte"])
    print(f"scikit-learn: {sklearn.__version__}")
    print(f"Peso MB: {MODEL_PATH.stat().st_size / 1e6:.6f}")
    print(f"Modelo guardado en: {MODEL_PATH}")

    return metricas


if __name__ == "__main__":
    entrenar()
