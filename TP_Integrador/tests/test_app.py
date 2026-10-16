import os
import unittest
from unittest.mock import patch

import gradio as gr

import app


class ClasificarResenaTests(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "INFERENCE_ENDPOINT_URL": "https://demo.hf.space/",
            "HF_TOKEN": "test-token",
        },
    )
    @patch("app.Client")
    def test_traduce_la_etiqueta_con_mayor_puntaje(self, cliente_mock):
        cliente_mock.return_value.predict.return_value = [
            {"label": "positive", "score": 0.91},
            {"label": "neutral", "score": 0.06},
            {"label": "negative", "score": 0.03},
        ]

        resultado = app.clasificar_resena("Muy buena atención")

        self.assertEqual(resultado, ("Positivo", "91.0%"))
        cliente_mock.assert_called_once_with(
            src="https://demo.hf.space/",
            hf_token="test-token",
            httpx_kwargs={"timeout": 120},
            verbose=False,
        )
        cliente_mock.return_value.predict.assert_called_once_with(
            "Muy buena atención",
            api_name="/clasificar",
        )

    @patch.dict(
        os.environ,
        {
            "INFERENCE_ENDPOINT_URL": "https://demo.hf.space/",
            "HF_TOKEN": "test-token",
        },
    )
    @patch("app.Client")
    def test_etiqueta_desconocida_se_informa(self, cliente_mock):
        cliente_mock.return_value.predict.return_value = [
            {"label": "LABEL_0", "score": 0.91},
        ]

        with self.assertRaises(gr.Error):
            app.clasificar_resena("Texto de prueba")

    @patch.dict(
        os.environ,
        {
            "INFERENCE_ENDPOINT_URL": "https://demo.hf.space/",
            "HF_TOKEN": "test-token",
        },
    )
    @patch("app.Client")
    def test_rechaza_formato_de_respuesta_inesperado(self, cliente_mock):
        cliente_mock.return_value.predict.return_value = {"label": "positive"}

        with self.assertRaises(gr.Error):
            app.clasificar_resena("Texto de prueba")

    def test_rechaza_resena_vacia(self):
        with self.assertRaises(gr.Error):
            app.clasificar_resena("   ")

    @patch.dict(os.environ, {}, clear=True)
    def test_informa_si_falta_la_url_del_endpoint(self):
        with self.assertRaises(gr.Error):
            app.clasificar_resena("Buena atención")

    @patch.dict(os.environ, {"INFERENCE_ENDPOINT_URL": "https://demo.hf.space/"}, clear=True)
    def test_informa_si_falta_el_token(self):
        with self.assertRaises(gr.Error):
            app.clasificar_resena("Buena atención")

    @patch.dict(
        os.environ,
        {
            "INFERENCE_ENDPOINT_URL": "https://ejemplo.invalid/",
            "HF_TOKEN": "test-token",
        },
    )
    @patch("app.Client")
    def test_no_envia_el_token_a_una_url_ajena(self, cliente_mock):
        with self.assertRaises(gr.Error):
            app.clasificar_resena("Buena atención")

        cliente_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
