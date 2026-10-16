# Clase 5: publicación y documentación

En esta actividad se publica el mismo creador de saludos con dos interfaces:
Gradio Blocks y Streamlit. Ambas llaman a `crear_saludo` desde `logica.py`, de
modo que la lógica es compartida y el cambio principal está en la interfaz.

## Archivos

- `logica.py`: función compartida que recibe nombre y estilo y devuelve un
  saludo.
- `gradio_app.py`: interfaz Gradio Blocks, preparada para usar el puerto que
  Render asigna mediante la variable `PORT`.
- `streamlit_app.py`: interfaz mínima equivalente en Streamlit.
- `requirements-gradio.txt`: dependencias de la aplicación para Render,
  incluidas las versiones compatibles con Gradio 5.0.0.
- `requirements.txt`: dependencia de Streamlit Community Cloud.
- `../render.yaml`: configuración declarativa de Render ubicada en la raíz del
  repositorio.
- `README.md`: esta guía de instalación, publicación y comparación.

## Probar localmente en Windows

Abrí PowerShell en la raíz del repositorio. Creá y activá un entorno para esta
clase:

```powershell
py -3.13 -m venv Clase_5\.venv
.\Clase_5\.venv\Scripts\Activate.ps1
```

Instalá las dependencias de la interfaz que quieras probar.

Para Gradio:

```powershell
python -m pip install -r Clase_5\requirements-gradio.txt
python Clase_5\gradio_app.py
```

Para Streamlit:

```powershell
python -m pip install -r Clase_5\requirements.txt
python -m streamlit run Clase_5\streamlit_app.py
```

Abrí la dirección local que indique el comando. En las dos versiones, escribí
un nombre, elegí **Informal** o **Formal** y creá el saludo. Para detener el
servidor, presioná `Ctrl+C` en la terminal.

> Cada interfaz usa su propio archivo de dependencias. No hace falta instalar
> las dos listas para probar una sola aplicación.

## Publicar Gradio en Render

Antes de desplegar, subí los archivos de la actividad a la rama de GitHub que
vas a publicar. Desde la raíz del repositorio, podés registrar solo los
archivos de esta entrega con:

```powershell
git status
git add .gitignore README.md render.yaml Clase_3/README.md Clase_5
git commit -m "Agregar actividad de publicación de clase 5"
git push
```

Revisá `git status` antes de confirmar para no incluir cambios de otras clases
que no quieras publicar.

El archivo `render.yaml` está en la raíz y configura un servicio web gratuito
con estos comandos:

- Instalación: `pip install -r Clase_5/requirements-gradio.txt`
- Inicio: `python Clase_5/gradio_app.py`

Pasos para publicarlo:

1. Subí los cambios de este repositorio a GitHub.
2. Iniciá sesión en Render y elegí **New > Blueprint**.
3. Conectá el repositorio de GitHub y seleccioná la rama que contiene estos
   cambios.
4. Render detectará `render.yaml`. Revisá la configuración y creá el servicio.
5. Esperá a que termine el despliegue y abrí la URL `onrender.com` del servicio.
   Probá ambos estilos de saludo.

## Publicar Streamlit Community Cloud

1. Subí los cambios a GitHub y confirmá que `Clase_5/streamlit_app.py`,
   `Clase_5/logica.py` y `Clase_5/requirements.txt` estén en la rama a publicar.
2. Iniciá sesión en [Streamlit Community Cloud](https://share.streamlit.io/) y
   elegí **Create app**.
3. Seleccioná este repositorio, la rama publicada y como archivo principal
   `Clase_5/streamlit_app.py`.
4. En la configuración avanzada, elegí Python 3.13 para que coincida con el
   entorno usado en la actividad y desplegá.
5. Cuando finalice la publicación, abrí la URL generada y probá los dos estilos.

Streamlit Community Cloud ejecuta la app desde la raíz del repositorio y busca
el archivo de dependencias junto al archivo principal; por eso
`Clase_5/requirements.txt` está junto a `streamlit_app.py`.

## Enlaces publicados

Completá esta sección con las direcciones que proporcionen las plataformas
después de desplegar y verificar las aplicaciones:

- **Gradio en Render:** pendiente de publicar.
- **Streamlit Community Cloud:** pendiente de publicar.

## Diferencias entre las herramientas

| Aspecto | Gradio Blocks | Streamlit |
|---|---|---|
| Enfoque | Componentes de entrada y salida conectados a funciones. | Aplicación de datos que se construye ejecutando Python de arriba hacia abajo. |
| Interacción de esta actividad | El evento del botón envía los valores de los componentes a `crear_saludo`. | Los widgets entregan sus valores; el botón controla cuándo se muestra el saludo. |
| Publicación elegida | Servicio web en Render, configurado en `render.yaml`. | Streamlit Community Cloud, configurado seleccionando el archivo principal en la plataforma. |
| Lógica de negocio | Compartida en `logica.py`. | Compartida en `logica.py`. |

## Checklist de entrega

- [x] Código de ambas interfaces y lógica común en el repositorio.
- [x] README de Clase 5 y README general del portfolio.
- [x] Configuración de Render preparada en `render.yaml`.
- [ ] Aplicación Gradio desplegada y probada en Render.
- [ ] Aplicación Streamlit desplegada y probada en Community Cloud.
- [ ] Enlaces públicos copiados en la sección **Enlaces publicados** y en el
      README general.

El despliegue necesita acceso a las cuentas de GitHub, Render y Streamlit
Community Cloud. Los enlaces quedan pendientes hasta completar esos pasos con
la cuenta del estudiante; este README no presenta como publicados servicios
que aún no se verificaron.
