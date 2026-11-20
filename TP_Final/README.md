# TP Final - Riesgo de abandono laboral

Proyecto completo con modelo propio de scikit-learn, API FastAPI y frontend HTML/CSS/JavaScript.

## Ejecutar localmente

Desde la raiz del repositorio:

```powershell
python -m pip install -r TP_Final/app/backend/requirements.txt
python TP_Final/notebook/entrenamiento.py
python -m uvicorn TP_Final.app.backend.main:app --reload --port 8080
```

Abrir `http://localhost:8080/`. La documentacion de la API queda en `http://localhost:8080/docs`.

## Ejecutar tests

```powershell
python -m pytest TP_Final/tests/test_app.py -q
```

## Estructura

```text
TP_Final/
├── app/
│   ├── frontend/
│   ├── backend/
│   └── modelo/
└── notebook/
```

## Dataset y modelo

El proyecto utiliza `WA_Fn-UseC_-HR-Employee-Attrition.csv`, un dataset de demostración de IBM HR distribuido en Kaggle. Contiene 1470 filas y 35 columnas; la etiqueta es `Attrition` (`Yes`/`No`). Es un dataset ficticio/de demostración, no registros reales de empleados de IBM.

El entrenamiento utiliza diez variables: `Age`, `Department`, `JobRole`, `MonthlyIncome`, `JobSatisfaction`, `YearsAtCompany`, `OverTime`, `DistanceFromHome`, `WorkLifeBalance` y `YearsSinceLastPromotion`. No se usan identificadores ni atributos como `Gender`.

El notebook de análisis `ibm-hr-analytics-employee-attrition-performance.ipynb` también lee el CSV local ubicado en la raíz de `TP_Final`. El notebook reproducible del proyecto es `notebook/entrenamiento.ipynb`.

Se comparan dos candidatos: Regresión Logística y Random Forest. La selección se realiza mediante F1 promedio en validación cruzada estratificada de 5 particiones sobre el conjunto de entrenamiento; el conjunto de prueba se reserva para la evaluación final. Ambos candidatos usan:

- `StandardScaler` para variables numéricas.
- `OneHotEncoder` para variables categóricas.
- División `80% / 20%` con estratificación.

El modelo final se exporta a `TP_Final/app/modelo/modelo.joblib`.
Los resultados actuales son:

- Modelo seleccionado: Random Forest.
- F1 medio de validación cruzada: 51.08% (desviación estándar 5.63 puntos porcentuales).
- Accuracy en prueba: 82.99%.
- Precision en prueba: 45.71%.
- Recall en prueba: 34.04%.
- F1 en prueba: 39.02%.
- ROC-AUC en prueba: 75.18%.

La prueba final contiene 294 registros y no se utiliza para seleccionar el modelo. El dataset está desbalanceado: 237 `Yes` y 1233 `No`; por eso Accuracy sola puede ser engañosa. En la matriz de confusión de prueba, el modelo detectó 16 de 47 casos `Yes`, omitió 31 y generó 19 falsas alarmas.

Para reentrenar, ejecutar desde la raíz del repositorio:

```powershell
python TP_Final/notebook/entrenamiento.py
```

El CSV debe permanecer en `TP_Final/WA_Fn-UseC_-HR-Employee-Attrition.csv`.

## Entregables

El generador produce `TPF_Bueno_Pereyra_Pedro.pdf` y `TPF_Bueno_Pereyra_Pedro.pptx`, siguiendo el formato de nombre de la consigna. La presentación tiene 10 diapositivas.

## API

- `GET /health`: informa el estado, el modelo cargado, la versión de scikit-learn y el CSV usado.
- `POST /predecir`: recibe el JSON del formulario y devuelve predicción, probabilidad y nivel de riesgo.
- Campos inválidos o incompletos: HTTP `422`.
- Errores internos: HTTP `500`.

## Deploy

La opción recomendada es publicar todo el servicio en Render:

1. Conectar el repositorio de GitHub.
2. Dejar **Root Directory** vacío para que los comandos se ejecuten desde la raíz del repositorio.
3. Build: `pip install -r TP_Final/app/backend/requirements.txt`.
4. Start: `uvicorn TP_Final.app.backend.main:app --host 0.0.0.0 --port $PORT`.
5. Render sirve el frontend desde `/` y la API desde `/health` y `/predecir`.

Como frontend y backend quedan en el mismo dominio no es necesario resolver CORS. El middleware CORS también está habilitado para permitir un frontend separado.

Para publicar frontend y backend por separado:

1. Publicar el backend en Render.
2. Copiar su URL HTTPS, por ejemplo `https://riesgo-abandono-empleados.onrender.com`.
3. Cambiar `api-base-url` en `app/frontend/index.html`:

```html
<meta name="api-base-url" content="https://riesgo-abandono-empleados.onrender.com">
```

4. Publicar `app/frontend` en GitHub Pages.
