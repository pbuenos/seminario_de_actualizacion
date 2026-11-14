import os
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from Clase_7 import logica


class ClasificarTests(unittest.TestCase):
    def test_pipeline_local_devuelve_etiqueta_y_puntaje(self):
        ejecutar_pipeline = Mock(
            return_value=[{"label": "POSITIVE", "score": 0.91}]
        )
        with patch.object(logica, "_cargar_pipeline", return_value=ejecutar_pipeline):
            resultado = logica.clasificar_local(" I love this ")

        self.assertEqual(resultado, ("POSITIVE", 0.91))
        ejecutar_pipeline.assert_called_once_with("I love this", truncation=True)

    def test_rechaza_texto_vacio_antes_de_cargar_el_pipeline(self):
        with patch.object(logica, "_cargar_pipeline") as cargar:
            with self.assertRaisesRegex(ValueError, "frase"):
                logica.clasificar_local("  ")

        cargar.assert_not_called()

    @patch.dict(os.environ, {}, clear=True)
    def test_api_informa_si_falta_el_token(self):
        with self.assertRaisesRegex(ValueError, "HF_TOKEN"):
            logica.clasificar_api("A test sentence")

    @patch.dict(os.environ, {"HF_TOKEN": "test-token"})
    def test_api_devuelve_la_clase_con_mayor_puntaje(self):
        respuesta = [
            SimpleNamespace(label="NEGATIVE", score=0.15),
            SimpleNamespace(label="POSITIVE", score=0.85),
        ]
        cliente = SimpleNamespace(text_classification=lambda texto: respuesta)
        crear_cliente = Mock(return_value=cliente)
        fake_hub = types.ModuleType("huggingface_hub")
        fake_hub.InferenceClient = crear_cliente
        with patch.dict(sys.modules, {"huggingface_hub": fake_hub}):
            resultado = logica.clasificar_api("A test sentence")

        self.assertEqual(resultado, ("POSITIVE", 0.85))
        crear_cliente.assert_called_once_with(model=logica.MODELO, token="test-token")


if __name__ == "__main__":
    unittest.main()
