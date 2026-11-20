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

El proyecto usa un dataset sintético y reproducible creado en `entrenamiento.py`. Es válido como dataset de prueba. Contiene 2000 registros y una variable objetivo binaria: `abandono`.

Se comparan dos candidatos: Regresión Logística y Random Forest. El pipeline selecciona automáticamente el modelo con mayor F1 para exportarlo. Ambos candidatos usan:

- `StandardScaler` para variables numéricas.
- `OneHotEncoder` para variables categóricas.
- División `80% / 20%` con estratificación.

El modelo final se exporta a `TP_Final/app/modelo/modelo.joblib`.
Los resultados actuales son:

- Accuracy: 60.25%.
- Precision: 60.09%.
- Recall: 65.69%.
- F1: 62.76%.
- ROC-AUC: 63.59%.
- F1 medio con validación cruzada de 5 particiones: 61.71%.

Random Forest fue seleccionado por tener el mayor F1 en la comparación.

## API

- `GET /health`: devuelve `{"estado": "ok"}`.
- `POST /predecir`: recibe el JSON del formulario y devuelve predicción, probabilidad y nivel de riesgo.
- Campos inválidos o incompletos: HTTP `422`.
- Errores internos: HTTP `500`.

## Deploy

La opción recomendada es publicar todo el servicio en Render:

1. Conectar el repositorio de GitHub.
2. Configurar el directorio raíz del servicio como `TP_Final/app/backend`.
3. Build: `pip install -r requirements.txt`.
4. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
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
