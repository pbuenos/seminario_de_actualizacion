# Trabajo Práctico Integrador: Semáforo de reseñas

Aplicación de análisis de sentimiento para explorar reseñas breves en español.
Recibe un texto y consulta un modelo ya entrenado que devuelve una etiqueta
(positivo, neutro o negativo) y su puntaje. La app **infiere**; no entrena ni
actualiza el modelo.

## Modelo y arquitectura

La aplicación usa
[`cardiffnlp/twitter-xlm-roberta-base-sentiment`](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment).
La interfaz se ejecuta en Render y consulta, con `gradio_client`, una Space
pública con ZeroGPU que ejecuta el modelo. Así Render no descarga ni mantiene
en memoria los pesos (el archivo de Cardiff ocupa alrededor de 1,11 GB).
ZeroGPU asigna una GPU durante la inferencia y depende de cuota y disponibilidad.

La notebook `Experimentos_modelos.ipynb` compara este modelo con
[`pysentimiento/robertuito-sentiment-analysis`](https://huggingface.co/pysentimiento/robertuito-sentiment-analysis)
usando las mismas frases etiquetadas manualmente. También contrasta
`pipeline` local con una llamada remota a la API Gradio mediante `gradio_client`.
La Space usa Gradio nativo porque ZeroGPU requiere una función Gradio decorada
con `@spaces.GPU`; por eso la app usa `gradio_client` en vez de
`InferenceClient` para llamar a esta Space. Es una adaptación de la arquitectura
por la compatibilidad del hardware elegido; tenelo presente al explicar la
decisión. Ejecutá todas las celdas para producir resultados y tiempos medidos
en tu propio entorno; no copies resultados supuestos.

## Ejecutar en Windows

Desde la raíz del repositorio:

```powershell
py -3.13 -m venv TP_Integrador\.venv
TP_Integrador\.venv\Scripts\python.exe -m pip install -r TP_Integrador\requirements.txt
$env:INFERENCE_ENDPOINT_URL = "https://USUARIO-NOMBRE-SPACE.hf.space/"
$env:HF_TOKEN = "tu_token_de_lectura_de_hugging_face"
TP_Integrador\.venv\Scripts\python.exe TP_Integrador\app.py
```

Primero desplegá el servicio de inferencia descrito en `hf_space/README.md` y
reemplazá el ejemplo por su URL pública. Creá un token gratuito de lectura en
Hugging Face; se usa como autenticación del cliente, no como crédito de
Inference Providers. La app solo lo envía a una URL HTTPS terminada en
`.hf.space`. En Render agregalo como secreto, no en el código ni en Git. Abrí
la dirección local que muestre Gradio. Para ejecutar las pruebas:

```powershell
TP_Integrador\.venv\Scripts\python.exe -m unittest discover -s TP_Integrador\tests -v
```

Para instalar también las dependencias de la notebook, usá
`TP_Integrador\requirements-notebook.txt` en lugar de `requirements.txt`. Las
celdas con `pipeline` descargan los modelos en tu computadora; Cardiff pesa
alrededor de 1,11 GB. Si tu equipo no tiene memoria suficiente, usá Colab.

## Informe y presentación

Se incluyen borradores de cinco páginas y siete diapositivas:
`TP_Apellido_Nombre.pdf` y `TP_Apellido_Nombre.pptx`. Están marcados como
borrador: faltan ejecutar el notebook, completar resultados reales, publicar
los servicios, agregar URLs y una captura de la app funcionando, y reemplazar
el nombre de ejemplo. No entregues esos archivos sin completar y verificar
esas evidencias.

El contenido se puede regenerar desde `TP_Integrador` con:

```powershell
python -m pip install -r requirements-documentos.txt
python generar_entregables.py
```

## Publicar en Render

El repositorio ya tiene un `render.yaml` en su raíz para otra actividad. Para
no cambiar esa configuración, creá este servicio desde el panel de Render:

1. Elegí **New > Web Service** y conectá el repositorio y la rama que contienen
   esta carpeta.
2. Configurá **Root Directory** como `TP_Integrador`.
3. Usá **Python 3** como entorno, `pip install -r requirements.txt` como
   comando de instalación y `python app.py` como comando de inicio.
4. En **Environment**, agregá `INFERENCE_ENDPOINT_URL` con la URL pública de
   la Space de inferencia y `HF_TOKEN` como secreto.
5. Creá el servicio, esperá a que el deploy termine y probá la URL pública con
   una reseña positiva, una negativa y una vacía.

Render entrega el puerto en la variable `PORT`; `app.py` la lee al iniciar.
En el plan gratuito el servicio se suspende tras 15 minutos sin tráfico y el
arranque puede tardar alrededor de un minuto. La Space puede tener cola,
inicio en frío o cuota diaria agotada en ZeroGPU. No se necesitan créditos de
Inference Providers: `gradio_client` llama a la API de la Space.

## Alcance y límites

- El puntaje es la confianza que reporta el modelo, no una probabilidad
  calibrada ni una garantía de acierto.
- Ironía, sarcasmo, jerga, textos muy cortos, errores de escritura y reseñas en
  idiomas distintos del español pueden producir errores.
- El modelo se ajustó para sentimiento en publicaciones de redes sociales
  multilingües; una reseña de comercio no necesariamente se parece a sus datos.
- La aplicación depende de Internet, de una Space pública disponible, de un
  token de lectura y de la cuota/disponibilidad de ZeroGPU.
  No está dimensionada para concurrencia o uso masivo.
- No debe utilizarse para decisiones automáticas sobre clientes y no se deben
  introducir datos personales.

## Estructura

- `app.py`: interfaz Gradio y llamada remota al modelo.
- `requirements.txt`: dependencias de la app, incluida la API de Gradio.
- `requirements-notebook.txt`: dependencias adicionales para ejecutar la
  comparación local con `pipeline`.
- `hf_space/`: servicio de modelo para publicar como una Space Gradio con
  ZeroGPU.
- `Experimentos_modelos.ipynb`: comparación reproducible, laboratorio y
  mediciones.
- `tests/test_app.py`: pruebas de la lógica de presentación de resultados.
- `TP_Apellido_Nombre.pdf` y `TP_Apellido_Nombre.pptx`: borradores de informe
  y presentación; requieren completar los resultados y evidencias reales.
- `generar_entregables.py` y `requirements-documentos.txt`: generación de los
  borradores en PDF y PowerPoint.

## Entrega y enlaces

- **App publicada:** completar después del deploy.
- **Carpeta del TP en GitHub:** completar con el enlace al repositorio.
- **Ayuda de IA generativa:** se usó como apoyo para proponer y documentar la
  estructura inicial, revisar código y preparar pruebas. Verificá cada
  resultado y declaralo con precisión en el informe y la presentación.

## Historial de commits

Registrá avances pequeños y comprobables en commits separados. Antes de cada
commit, revisá `git status` y agregá solo archivos de `TP_Integrador`; evitá
incluir los cambios de otras clases.
