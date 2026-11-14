# Clase 11: publicación de modelos en Hugging Face

## Repositorios publicados

- [scikit-learn](https://huggingface.co/Pbueno467/regresion-casas-sklearn)
- [PyTorch](https://huggingface.co/Pbueno467/regresion-casas-pytorch)
- [Keras](https://huggingface.co/Pbueno467/regresion-casas-keras)
- [Transformers](https://huggingface.co/Pbueno467/clasificador-comentarios-transformers)

## 1. ¿Cómo subí los archivos? ¿Usé un token?

Subí los archivos desde la web de Hugging Face con **Upload files**, por lo que
no necesité crear ni guardar un token. Un token no debe escribirse en el código
ni subirse a GitHub porque es una credencial: quien lo obtenga podría usar los
permisos concedidos a la cuenta.

## 2. ¿Qué etiquetas aparecen y de dónde salen?

Los metadatos declarados salen del bloque YAML al principio de cada
`README.md`: `library_name`, `pipeline_tag`, `tags`, `language` y `license`.
Hugging Face también muestra etiquetas de biblioteca o formato, como Joblib y
Safetensors.

| Modelo | Etiquetas visibles |
|---|---|
| scikit-learn | Tabular Regression, Scikit-learn, Joblib, Spanish, machine-learning, regression, linear-regression, educational-example, License: mit |
| PyTorch | Tabular Regression, PyTorch, Safetensors, Spanish, machine-learning, regression, linear-regression, educational-example, License: mit |
| Keras | Tabular Regression, Keras, Spanish, machine-learning, regression, linear-regression, educational-example, License: mit |
| Transformers | Text Classification, Transformers, Safetensors, Spanish, bert, machine-learning, educational-example, text-embeddings-inference, License: mit |

Las tres regresiones declaran `pipeline_tag: tabular-regression`; Transformers
declara `pipeline_tag: text-classification`. Las etiquetas de biblioteca y
formato que muestra el Hub no necesariamente están escritas literalmente en
la lista `tags`.

## 3. ¿Cuál es el modelo entrenado y qué archivos se usan o reproducen?

| Biblioteca | Archivo del modelo entrenado | Para usar el modelo | Para reproducir el entrenamiento |
|---|---|---|---|
| scikit-learn | `model.joblib`, que contiene el pipeline serializado. | `model.joblib` y sus dependencias; el pipeline incluye el preprocesamiento. `predict.py` y `predict_hub.py` muestran cómo predecir. | `train.py` y `requirements.txt`; el script genera los datos sintéticos y entrena el modelo. |
| PyTorch | `model.safetensors`, que guarda los pesos. | También hacen falta `config.json`, `modelo.py` y las dependencias para reconstruir la arquitectura y normalizar las entradas. | `train.py`, `modelo.py`, `config.json` y `requirements.txt`. |
| Keras | `model.keras`, que guarda la estructura y los pesos. | `model.keras` y las dependencias de Keras; la normalización está dentro del modelo. | `train.py` y `requirements.txt`. |
| Transformers | `model.safetensors`, que guarda los pesos. | También hacen falta `config.json`, `tokenizer.json`, `tokenizer_config.json` y Transformers. | `train.py`, los archivos del tokenizer, la configuración y `requirements.txt`. |

`predict.py` usa archivos locales. `predict_hub.py` descarga el modelo del Hub y
ejecuta la predicción en la computadora; no vuelve a entrenarlo.

Probé los cuatro `predict_hub.py`. scikit-learn y PyTorch predijeron
aproximadamente 94.7, 148.5 y 205.5 miles de US$; Keras, 94.6, 148.6 y 205.6
miles de US$. Transformers clasificó las tres frases de ejemplo como
`positivo`, `negativo` y `positivo`.

## 4. ¿Qué guardan los dos `config.json`?

No guardan lo mismo. El `config.json` de PyTorch es propio del ejemplo y
describe la arquitectura de regresión, las variables de entrada y salida y
los valores de media y desvío para normalizar las entradas. El de Transformers
describe la configuración de BERT, por ejemplo sus dimensiones, capas y
etiquetas (`id2label` y `label2id`), para reconstruir el modelo junto con sus
pesos.

## 5. ¿Por qué PyTorch necesita `modelo.py` y Keras no?

`model.safetensors` de PyTorch guarda los valores de los tensores, pero no la
clase `RegresionLineal` ni su método `forward`. `modelo.py` define esa
arquitectura para poder cargar los pesos. En cambio, `model.keras` serializa
la estructura del modelo Keras y sus pesos, incluida la capa de normalización;
por eso no necesita una clase Python aparte.

## 6. ¿Se puede usar alguno con `InferenceClient` como Cardiff?

No en la configuración actual. Las páginas de los cuatro modelos indican que
no están desplegados por ningún **Inference Provider**. Transformers tiene la
tarea `text-classification`, pero eso por sí solo no despliega un servicio.
Los `predict_hub.py` descargan los archivos y ejecutan la inferencia
localmente; no usan `InferenceClient`.

## 7. ¿Aparece **Use this model** y funciona el código sugerido?

| Modelo | Resultado |
|---|---|
| scikit-learn | El botón aparece y ofrece Scikit-learn, Colab y Kaggle. El snippet busca `sklearn_model.joblib`, pero el archivo publicado se llama `model.joblib`; no funcionaría sin corregir ese nombre. `predict_hub.py`, que usa el nombre correcto, sí funcionó. |
| PyTorch | El botón no aparece en la página. La predicción sí funcionó con `predict_hub.py`. |
| Keras | El botón aparece. El snippet usa `keras.saving.load_model("hf://...")`; para este archivo `.keras`, el ejemplo `predict_hub.py` descarga `model.keras` con `hf_hub_download` y lo carga desde la ruta local. Esa prueba funcionó. |
| Transformers | El botón aparece y ofrece un ejemplo con `pipeline`. La prueba con `predict_hub.py`, que usa `pipeline` con ese repo, funcionó. No probé por separado el segundo snippet con `AutoTokenizer` y `AutoModelForSequenceClassification`. |

## 8. ¿Qué necesita otra persona para usar el modelo PyTorch?

Además de `model.safetensors`, necesita PyTorch, `safetensors`, `modelo.py`
con la clase `RegresionLineal` y `config.json` con la normalización. Debe
ingresar las variables en el orden `m2`, `balcon`, `ascensor`, crear la
arquitectura, cargarle los pesos y aplicar la media y el desvío antes de
predecir. Puede guiarse por `predict.py` o `predict_hub.py`.

## 9. ¿Dónde más se podría compartir un modelo?

Se podría compartir en GitHub o GitLab, en un registro como MLflow o como
archivo descargable en la nube. Hugging Face Hub está especializado en modelos:
reúne archivos, versiones, Model Cards, etiquetas de tareas y ejemplos de uso.
En un repositorio o almacenamiento genérico habría que organizar esa
documentación y las instrucciones de carga por separado.
