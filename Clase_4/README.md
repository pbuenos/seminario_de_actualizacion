---
title: Mi App
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.0.0
app_file: Clase_4/app.py
---

# Clase 4: Gradio Blocks

Esta aplicación permite crear un saludo personalizado con Gradio. La interfaz
está construida con `gr.Blocks`, un campo de texto, un menú desplegable, un
botón y un campo de resultado.

## Archivos de la carpeta

- `app.py`: aplicación Gradio y función `crear_saludo(nombre, estilo)`.
- `requirements.txt`: dependencias de la aplicación. Incluye la compatibilidad
  de audio para Python 3.13 o superior y versiones compatibles de FastAPI,
  Starlette y `huggingface-hub` para Gradio 5.0.0.
- `README.md`: esta guía y la configuración de Gradio Spaces.
- `Clase_4_Presentacion.pptx`: presentación de la clase.
- `index.html` y `style.css`: archivos de una plantilla estática; no son usados
  por la aplicación Gradio de `app.py`.
- `.gitignore`: reglas para ignorar archivos en Git.
- `.gitattributes`: reglas de Git LFS para archivos binarios grandes.
- `.gitkeep`: archivo vacío para conservar la carpeta en Git.

## Ejecutar la aplicación en Windows

Abrí una terminal de PowerShell en esta carpeta. Si estás en la carpeta raíz
del curso, ingresá con:

```powershell
cd "Clase_4"
```

Creá el entorno virtual con Python 3.13:

```powershell
py -3.13 -m venv .venv
```

Si `.venv` ya existe, no hace falta volver a crearlo. En VS Code, seleccioná
el intérprete `Clase_4\.venv\Scripts\python.exe` desde **Python: Select
Interpreter** (`Ctrl+Shift+P`). Usar la ruta completa del intérprete en los
comandos siguientes ayuda a no instalar las dependencias en el entorno de otra
clase.

La dependencia `audioop-lts` se instala automáticamente en Python 3.13 o
superior para resolver la compatibilidad de audio de Gradio 5.0.0. No hace
falta instalarla manualmente. Las versiones de FastAPI y Starlette también
están fijadas para que la página de Gradio renderice correctamente.

Instalá las dependencias y ejecutá la aplicación:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

La terminal mostrará una dirección local; abrila en el navegador para probar
la aplicación. Escribí un nombre, elegí **Informal** o **Formal** y presioná
**Crear saludo**. La función devuelve el saludo en el campo **Resultado**.
También muestra un mensaje si el nombre está vacío.

Para detener la aplicación, volvé a la terminal y presioná `Ctrl+C`.
