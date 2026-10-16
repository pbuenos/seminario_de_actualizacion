---
title: Semáforo de reseñas - API
emoji: 🧪
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.0.0
app_file: app.py
python_version: 3.12
---

# Servicio de inferencia del Semáforo de reseñas

Esta Space usa una aplicación Gradio nativa y ejecuta el modelo en ZeroGPU.
Render y la notebook se conectan a su API Gradio mediante `gradio_client`.

La Space debe ser pública para que Render pueda conectarse con un token de
lectura. ZeroGPU asigna la GPU al ejecutar la función de clasificación; su
disponibilidad y cuota dependen de las condiciones vigentes de Hugging Face.

## Crear la Space

1. En Hugging Face, creá una Space nueva y seleccioná el SDK **Gradio**.
2. En hardware, seleccioná **ZeroGPU** si la cuenta lo permite.
3. Subí el contenido de esta carpeta (`README.md`, `app.py` y
   `requirements.txt`) al repositorio de la Space. No subas tokens.
4. Esperá a que termine el build. Probá la interfaz y copiá el dominio público
   que termina en `.hf.space`.
5. Configurá `INFERENCE_ENDPOINT_URL` en Render y en tu entorno local con ese
   dominio, incluyendo la barra final. Guardá `HF_TOKEN` como secreto.

## API Gradio

La función `clasificar` está expuesta como `/clasificar` y devuelve una lista
de etiquetas y puntajes. La app de Render la llama con
`Client.predict(texto, api_name="/clasificar")`.
