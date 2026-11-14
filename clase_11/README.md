# Clase 11: publicar cuatro modelos en Hugging Face

La consigna pide publicar cada modelo del repositorio de ejemplos en **su
propio repositorio de tipo Model** y verificar su Model Card. No hace falta
entrenar un cuarto modelo: el cuarto es el clasificador de Transformers.

Repositorio de ejemplos de la cátedra:
[`cynthiavillagra/ifts18-practica-model-cards`](https://github.com/cynthiavillagra/ifts18-practica-model-cards).
Cada carpeta incluye un `README.md` con metadatos de Model Card. Conservá el
contenido y la licencia MIT del material al subirlo.

## Los cuatro repositorios

Creá cuatro repositorios distintos en Hugging Face, uno por carpeta. Los
nombres sugeridos usan `TU-USUARIO` como marcador; reemplazalo por tu usuario.
Abrí cada carpeta del [repositorio de ejemplos](https://github.com/cynthiavillagra/ifts18-practica-model-cards)
para revisar sus archivos:

| Carpeta de origen | Nombre sugerido | Archivos propios de ese modelo |
|---|---|---|
| [`01-sklearn-regresion`](https://github.com/cynthiavillagra/ifts18-practica-model-cards/tree/main/01-sklearn-regresion) | `regresion-casas-sklearn` | `model.joblib` |
| [`02-pytorch-regresion`](https://github.com/cynthiavillagra/ifts18-practica-model-cards/tree/main/02-pytorch-regresion) | `regresion-casas-pytorch` | `model.safetensors`, `config.json`, `modelo.py` |
| [`03-keras-regresion`](https://github.com/cynthiavillagra/ifts18-practica-model-cards/tree/main/03-keras-regresion) | `regresion-casas-keras` | `model.keras` |
| [`04-transformers-clasificacion-texto`](https://github.com/cynthiavillagra/ifts18-practica-model-cards/tree/main/04-transformers-clasificacion-texto) | `
` | `model.safetensors`, `config.json`, `tokenizer.json`, `tokenizer_config.json` |

Además, las cuatro carpetas incluyen `README.md`, `train.py`, `predict.py`,
`predict_hub.py`, `requirements.txt` y `.gitignore`. Para cumplir la consigna,
subí el contenido de cada carpeta a su repo correspondiente. No subas el ZIP
entero cuatro veces ni mezcles archivos de distintos modelos.

## Publicar desde la web

La web es la opción más sencilla y no requiere crear un token:

### A. Preparar los archivos de origen

1. Abrí el repositorio de ejemplos en GitHub y elegí **Code** → **Download ZIP**.
2. Descomprimí el ZIP en una carpeta fácil de encontrar.
3. Identificá las cuatro carpetas de la tabla anterior.
4. Para la primera carga, seleccioná **los archivos que están dentro** de
   `01-sklearn-regresion`, no la carpeta contenedora ni todo el repositorio.
   Repetí el mismo criterio con cada una de las otras carpetas.

### B. Crear el primer repo en Hugging Face

1. Iniciá sesión y abrí [huggingface.co/new](https://huggingface.co/new).
2. En **Owner**, verificá que esté seleccionado tu usuario.
3. En **Repository name**, escribí `regresion-casas-sklearn`.
4. Elegí el tipo **Model**. No elijas **Dataset** ni **Space**.
5. Si la consigna no determina la visibilidad, confirmalo con el docente. Para
   que otras personas puedan abrir tu Model Card, el repositorio debe ser
   accesible para ellas.
6. Conservá la licencia MIT que declara el `README.md` del ejemplo, y creá el
   repositorio.

### C. Subir los archivos

1. Dentro del repositorio recién creado, abrí **Files and versions** → **Add
   file** → **Upload files** (los rótulos pueden variar un poco).
2. Arrastrá todos los archivos de `01-sklearn-regresion`. En particular,
   comprobá que estén `README.md` y `model.joblib`; también subí los scripts y
   `requirements.txt` de esa carpeta.
3. Asegurate de que los archivos queden en la raíz del repo de Hugging Face.
   El `README.md` y los artefactos no deberían quedar dentro de una carpeta
   extra `01-sklearn-regresion/`.
4. Escribí un mensaje de commit descriptivo, por ejemplo `Subir modelo sklearn
   de regresión`, y confirmá la carga.
5. Repetí **B** y **C** con estos nombres y carpetas:

   | Repo | Carpeta que tenés que cargar | Comprobá especialmente |
   |---|---|---|
   | `regresion-casas-pytorch` | `02-pytorch-regresion` | `model.safetensors`, `config.json` y `modelo.py` |
   | `regresion-casas-keras` | `03-keras-regresion` | `model.keras` |
   | `clasificador-comentarios-transformers` | `04-transformers-clasificacion-texto` | `model.safetensors`, `config.json` y los dos archivos del tokenizer |

6. Guardá las cuatro URLs. Por ejemplo:
   `https://huggingface.co/TU-USUARIO/regresion-casas-sklearn`.
   Anotalas en el registro de [`CUESTIONARIO.md`](./CUESTIONARIO.md).

**Importante:** no borres ni reemplaces el bloque YAML que aparece al comienzo
de cada `README.md` (entre dos líneas `---`). Ahí están `library_name`,
`pipeline_tag`, `tags`, idioma y licencia, que alimentan los metadatos de la
Model Card. Conservá también la atribución y el contenido del README original.

### Si preferís usar un token

La carga web no necesita un token. Si elegís VS Code o Git, creá un token con
permiso de escritura sobre los repositorios de modelos que vas a publicar (por
ejemplo, un token fine-grained limitado a esos repositorios). Guardalo en el
administrador de credenciales o en una variable de entorno local. No lo pongas
en un `.py`, notebook, `README.md`, captura ni commit: quien lo obtenga podría
usar los permisos de tu cuenta. En la pregunta 1, describí el método y el lugar
donde lo guardaste, pero nunca copies el valor del token.

## Después de publicar

Hacé esta verificación para cada uno de los cuatro repositorios:

1. En **Files and versions**, confirmá que los archivos estén en la raíz y que
   no hayas subido por error la carpeta de otro modelo.
2. Abrí **Model card**. Comprobá que se renderice el título y la descripción
   del `README.md`, y que arriba aparezcan etiquetas coherentes con esa tarea.
   Si solo ves el texto YAML sin formato, revisá que el README empiece con
   `---`, esté completo y se llame exactamente `README.md`.
3. Compará los nombres en la web con los de la tabla de archivos. En PyTorch y
   Transformers, no olvides el `config.json`; en Transformers, revisá además
   los archivos del tokenizer.
4. Buscá **Use this model**. Anotá si aparece y qué código ofrece; si está
   disponible, probalo y anotá cualquier ajuste o error. La aparición del
   botón no garantiza que el fragmento funcione sin dependencias, entradas o
   código auxiliar.
5. Copiá la URL y completá la tabla y las respuestas de
   [`CUESTIONARIO.md`](./CUESTIONARIO.md). Escribí lo que observaste realmente.

### Prueba opcional de predicción

No necesitás volver a entrenar los modelos para cumplir la publicación. Si
querés comprobar que uno se puede usar desde el Hub, ejecutá su `predict_hub.py`
desde la carpeta de ese ejemplo, después de instalar ese `requirements.txt`.
Por ejemplo, dentro de `01-sklearn-regresion`:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe predict_hub.py TU-USUARIO/regresion-casas-sklearn
```

Reemplazá el usuario y el nombre del repo. Este script descarga los archivos y
hace la predicción en tu PC; no es una llamada a un servicio remoto. Para
PyTorch y Keras, seguí el `requirements.txt` y el `predict_hub.py` de su propia
carpeta.

## Qué significa cada modelo

- **scikit-learn:** `model.joblib` es un pipeline serializado. `train.py`
  genera los datos sintéticos y vuelve a entrenar; `predict_hub.py` descarga
  el pipeline publicado para usarlo.
- **PyTorch:** `model.safetensors` guarda los pesos; `modelo.py` define la
  arquitectura y `config.json` aporta, entre otras cosas, el orden de las
  variables y la normalización necesaria para predecir.
- **Keras:** `model.keras` guarda la estructura y los pesos; la normalización
  está dentro del modelo serializado.
- **Transformers:** `model.safetensors` guarda los pesos; `config.json`
  describe BERT y sus etiquetas; `tokenizer.json` y `tokenizer_config.json`
  permiten convertir texto a las entradas del modelo.

Publicar los pesos en el Hub no significa que Hugging Face ya esté ejecutando
el modelo como un servicio de inferencia. `InferenceClient` requiere que un
proveedor compatible ofrezca ese modelo y esa tarea. Los scripts
`predict_hub.py` de los ejemplos descargan los archivos y ejecutan la
predicción en tu propia PC.

## Estado

Las guías están preparadas; los cuatro repositorios y sus enlaces quedan
pendientes de crear y verificar con tu cuenta.
