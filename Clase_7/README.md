# Clase 7: pipeline local e Inference API

La actividad compara dos formas de ejecutar el mismo clasificador de
sentimiento, usando dos interfaces en cada modalidad:

| Archivo | Interfaz | Ejecución del modelo |
|---|---|---|
| `app_gradio_local.py` | Gradio | En esta computadora |
| `app_streamlit_local.py` | Streamlit | En esta computadora |
| `app_gradio_api.py` | Gradio | En Hugging Face Inference Providers |
| `app_streamlit_api.py` | Streamlit | En Hugging Face Inference Providers |

Las cuatro aplicaciones usan
[`distilbert/distilbert-base-uncased-finetuned-sst-2-english`](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english).
Es un modelo binario preparado para inglés: puede equivocarse con español,
ironía, negaciones y frases ambiguas. Un puntaje alto no garantiza que la
interpretación sea correcta.

## Preparar el entorno en Windows

Desde la raíz del repositorio, creá un entorno propio para esta clase:

```powershell
py -3.13 -m venv Clase_7\.venv
```

Para las aplicaciones locales, que descargan los pesos y ejecutan el modelo en
tu computadora:

```powershell
Clase_7\.venv\Scripts\python.exe -m pip install -r Clase_7\requirements-local.txt
```

Para las aplicaciones con API, que requieren Internet y un token:

```powershell
Clase_7\.venv\Scripts\python.exe -m pip install -r Clase_7\requirements-api.txt
```

Las dos listas se pueden instalar en el mismo entorno. No compartas ni subas
`.venv`, tokens ni otros secretos.

## Ejecutar las aplicaciones locales

Gradio:

```powershell
Clase_7\.venv\Scripts\python.exe Clase_7\app_gradio_local.py
```

Streamlit:

```powershell
Clase_7\.venv\Scripts\python.exe -m streamlit run Clase_7\app_streamlit_local.py
```

La primera ejecución puede tardar mientras se descarga el modelo. Estas apps
usan CPU por defecto y el tiempo depende del equipo.

## Ejecutar las aplicaciones con Inference API

Creá en Hugging Face un token con permiso para consultar Inference Providers.
Los siguientes comandos piden el token de forma oculta y lo mantienen solo en
el proceso local; no lo escribas en el código ni en Git.

Gradio:

```powershell
Clase_7\.venv\Scripts\python.exe -c "import os, runpy; from getpass import getpass; os.environ['HF_TOKEN']=getpass('Token de Hugging Face: '); runpy.run_path('Clase_7/app_gradio_api.py', run_name='__main__')"
```

Streamlit:

```powershell
Clase_7\.venv\Scripts\python.exe -c "import os, sys, runpy; from getpass import getpass; os.environ['HF_TOKEN']=getpass('Token de Hugging Face: '); sys.argv=['streamlit','run','Clase_7/app_streamlit_api.py']; runpy.run_module('streamlit', run_name='__main__')"
```

Si no configurás `HF_TOKEN`, la aplicación informa qué falta. La llamada remota
depende del permiso del token, de la disponibilidad del proveedor y de sus
cuotas o condiciones de uso.

## Pruebas y comparación

Ejecutá las pruebas unitarias desde la raíz:

```powershell
Clase_7\.venv\Scripts\python.exe -m unittest discover -s Clase_7\tests -v
```

Probá frases en inglés, por ejemplo una positiva y otra negativa. Anotá las
etiquetas y puntajes que obtengas realmente. No compares porcentajes como si
fueran una medida de precisión: el puntaje expresa la confianza del modelo para
su predicción y la app no calcula exactitud.

La diferencia principal es dónde corre el modelo. Con `pipeline`, la
computadora descarga y mantiene los pesos localmente. Con `InferenceClient`,
la computadora envía la frase al servicio remoto y recibe su resultado. Las
interfaces son las mismas para que la comparación se concentre en la ejecución.
Al usar una API, no envíes textos privados o datos personales.
