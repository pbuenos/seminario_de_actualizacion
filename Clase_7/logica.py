import os
from functools import lru_cache


MODELO = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"


def _validar_texto(texto: str) -> str:
    texto = texto.strip()
    if not texto:
        raise ValueError("Escribí una frase para analizar.")
    return texto


@lru_cache(maxsize=1)
def _cargar_pipeline():
    from transformers import pipeline

    return pipeline("text-classification", model=MODELO)


def clasificar_local(texto: str) -> tuple[str, float]:
    texto = _validar_texto(texto)
    resultado = _cargar_pipeline()(texto, truncation=True)[0]
    return str(resultado["label"]), float(resultado["score"])


def clasificar_api(texto: str) -> tuple[str, float]:
    texto = _validar_texto(texto)
    token = os.environ.get("HF_TOKEN", "").strip()
    if not token:
        raise ValueError(
            "Falta HF_TOKEN. Configurá un token de Hugging Face con permiso "
            "para consultar Inference Providers."
        )

    from huggingface_hub import InferenceClient

    cliente = InferenceClient(model=MODELO, token=token)
    resultados = cliente.text_classification(texto)
    if not resultados:
        raise RuntimeError("Hugging Face devolvió una respuesta vacía.")

    mejor = max(resultados, key=lambda resultado: resultado.score)
    return str(mejor.label), float(mejor.score)
