"""Genera el dataset sintetico, entrena y exporta el modelo."""

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
MODEL_PATH = ROOT / "app" / "modelo" / "modelo.joblib"
RANDOM_SEED = 42


def crear_dataset(cantidad: int = 2000) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_SEED)

    edad = rng.integers(20, 61, cantidad)
    salario = rng.normal(3500, 1500, cantidad).clip(1200, 9000).round(2)
    antiguedad = np.minimum(rng.integers(0, 31, cantidad), edad - 18)
    satisfaccion = rng.integers(1, 5, cantidad)
    equilibrio = rng.integers(1, 5, cantidad)
    horas_extras = rng.choice(["Yes", "No"], cantidad, p=[0.28, 0.72])
    distancia = rng.integers(1, 61, cantidad)
    promocion = rng.integers(0, 16, cantidad)
    departamento = rng.choice(
        ["Ventas", "Investigacion y Desarrollo", "Recursos Humanos"],
        cantidad,
        p=[0.38, 0.50, 0.12],
    )
    rol = rng.choice(
        ["Ejecutivo comercial", "Cientifico", "Analista", "Gerente", "Especialista"],
        cantidad,
    )

    puntaje = (
        -1.2
        + (edad < 30) * 0.55
        + (horas_extras == "Yes") * 1.15
        + (satisfaccion == 1) * 1.0
        + (satisfaccion == 2) * 0.55
        + (equilibrio == 1) * 0.65
        + (antiguedad < 2) * 0.45
        + (promocion > 7) * 0.45
        + (distancia > 35) * 0.30
        - (salario > 6000) * 0.35
    )
    probabilidad = 1 / (1 + np.exp(-puntaje))
    abandono = (rng.random(cantidad) < probabilidad).astype(int)

    return pd.DataFrame(
        {
            "edad": edad,
            "departamento": departamento,
            "rol": rol,
            "salario_mensual": salario,
            "satisfaccion_laboral": satisfaccion,
            "anos_en_la_empresa": antiguedad,
            "horas_extras": horas_extras,
            "distancia_al_hogar": distancia,
            "equilibrio_vida_trabajo": equilibrio,
            "anos_desde_ultimo_ascenso": promocion,
            "abandono": abandono,
        }
    )


def entrenar() -> dict:
    datos = crear_dataset()
    objetivo = "abandono"
    features = [columna for columna in datos.columns if columna != objetivo]
    X = datos[features]
    y = datos[objetivo]

    X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_SEED,
        stratify=y,
    )

    categoricas = ["departamento", "rol", "horas_extras"]
    numericas = [columna for columna in features if columna not in categoricas]

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

    resultados = {}
    for nombre, candidato in candidatos.items():
        candidato.fit(X_entrenamiento, y_entrenamiento)
        predicciones_candidato = candidato.predict(X_prueba)
        probabilidades_candidato = candidato.predict_proba(X_prueba)[:, 1]
        resultados[nombre] = {
            "modelo": candidato,
            "accuracy": accuracy_score(y_prueba, predicciones_candidato),
            "precision": precision_score(
                y_prueba, predicciones_candidato, zero_division=0
            ),
            "recall": recall_score(y_prueba, predicciones_candidato, zero_division=0),
            "f1": f1_score(y_prueba, predicciones_candidato, zero_division=0),
            "roc_auc": roc_auc_score(y_prueba, probabilidades_candidato),
            "probabilidades": probabilidades_candidato,
        }

    modelo_nombre = max(resultados, key=lambda nombre: resultados[nombre]["f1"])
    modelo = resultados[modelo_nombre]["modelo"]
    predicciones = modelo.predict(X_prueba)
    probabilidades = modelo.predict_proba(X_prueba)[:, 1]
    validacion_cruzada = cross_val_score(
        modelo,
        X,
        y,
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED),
        scoring="f1",
    )
    metricas = {
        "accuracy": accuracy_score(y_prueba, predicciones),
        "precision": precision_score(y_prueba, predicciones, zero_division=0),
        "recall": recall_score(y_prueba, predicciones, zero_division=0),
        "f1": f1_score(y_prueba, predicciones, zero_division=0),
        "roc_auc": roc_auc_score(y_prueba, probabilidades),
        "f1_validacion_cruzada": float(validacion_cruzada.mean()),
        "matriz_confusion": confusion_matrix(y_prueba, predicciones).tolist(),
        "reporte": classification_report(y_prueba, predicciones),
        "modelo_seleccionado": modelo_nombre,
        "comparacion_modelos": {
            nombre: {
                clave: round(valor, 4)
                for clave, valor in resultado.items()
                if clave in {"accuracy", "precision", "recall", "f1", "roc_auc"}
            }
            for nombre, resultado in resultados.items()
        },
    }

    payload = {
        "model": modelo,
        "feature_names": features,
        "categorical_features": categoricas,
        "sklearn_version": sklearn.__version__,
        "model_name": modelo_nombre,
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, MODEL_PATH)

    print("Dataset: 2000 filas sinteticas creadas reproduciblemente")
    print("Division: 80% entrenamiento / 20% prueba")
    print("Comparacion de modelos:")
    for nombre, metricas_candidato in metricas["comparacion_modelos"].items():
        print(f"  {nombre}: {metricas_candidato}")
    print(f"Modelo seleccionado: {modelo_nombre}")
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
