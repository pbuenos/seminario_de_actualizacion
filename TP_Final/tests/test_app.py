from pathlib import Path
import sys

from fastapi.testclient import TestClient


BACKEND_DIR = Path(__file__).resolve().parents[1] / "app" / "backend"
sys.path.insert(0, str(BACKEND_DIR))

import main


client = TestClient(main.app)


def empleado_valido():
    return {
        "edad": 29,
        "departamento": "Sales",
        "rol": "Sales Executive",
        "salario_mensual": 3200,
        "satisfaccion_laboral": 3,
        "anos_en_la_empresa": 2,
        "horas_extras": "Yes",
        "distancia_al_hogar": 15,
        "equilibrio_vida_trabajo": 3,
        "anos_desde_ultimo_ascenso": 1,
    }


def test_health():
    respuesta = client.get("/health")
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == "ok"
    assert "modelo" in cuerpo
    assert "scikit_learn" in cuerpo
    assert cuerpo["dataset"] == "WA_Fn-UseC_-HR-Employee-Attrition.csv"


def test_predecir():
    respuesta = client.post("/predecir", json=empleado_valido())
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["prediccion"] in {
        "Probable abandono",
        "Probable permanencia",
    }
    assert 0 <= cuerpo["probabilidad"] <= 1
    assert cuerpo["riesgo"] in {"Bajo", "Medio", "Alto"}


def test_campo_faltante_devuelve_422():
    datos = empleado_valido()
    del datos["edad"]
    respuesta = client.post("/predecir", json=datos)
    assert respuesta.status_code == 422


def test_tipo_incorrecto_devuelve_422():
    datos = empleado_valido()
    datos["edad"] = "veinte"
    respuesta = client.post("/predecir", json=datos)
    assert respuesta.status_code == 422


def test_categoria_valida_del_dataset_se_acepta():
    datos = empleado_valido()
    datos["departamento"] = "Research & Development"
    datos["rol"] = "Manager"
    respuesta = client.post("/predecir", json=datos)
    assert respuesta.status_code == 200


def test_categoria_ajena_al_dataset_devuelve_422():
    datos = empleado_valido()
    datos["rol"] = "Analista"
    respuesta = client.post("/predecir", json=datos)
    assert respuesta.status_code == 422
