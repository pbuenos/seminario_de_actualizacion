# Clase 2: preparación del entorno y primer proyecto

Esta carpeta reúne los archivos de la práctica sobre Python, VS Code, entornos
virtuales, dependencias y Git.

## Archivos de esta carpeta

- `app.py`: programa de ejemplo. Importa `requests` y muestra su versión para
  comprobar que la biblioteca está disponible en el entorno de Python elegido.
- `requirements.txt`: lista las bibliotecas que necesita el proyecto y las
  versiones registradas. En esta práctica incluye `requests`.
- `.gitignore`: indica a Git qué archivos no debe registrar, como `.venv/` y
  los archivos compilados de Python (`__pycache__/`, `*.pyc`).
- `Clase_2_Presentacion.pdf`: material de presentación de la clase.
- `README.md`: esta guía, con una descripción de los archivos y los pasos de
  la práctica.
- `.venv/` (si ya la creaste): entorno virtual local de Python. Se genera
  durante la práctica, no se comparte en Git y está excluido por `.gitignore`.

## Guía de la práctica

Los comandos siguientes son para PowerShell. Abrí una terminal en VS Code y
ubicáte en esta carpeta:

```powershell
cd "ruta\al\proyecto\Clase_2"
```

### 1. Verificar Python, VS Code y Git; configurar el nombre de Git

Comprobá que las herramientas estén instaladas:

```powershell
py --version
code --version
git --version
```

Si `py` no está disponible, probá `python --version`. Para que Git identifique
tus commits, configurá tu nombre y correo (reemplazá los ejemplos):

```powershell
git config --global user.name "Tu nombre"
git config --global user.email "tu-correo@ejemplo.com"
```

Podés verificar la configuración con:

```powershell
git config --global --get user.name
git config --global --get user.email
```

### 2. Crear el proyecto con `app.py` y `README.md`

Abrí la carpeta del proyecto en VS Code. Desde el Explorador de archivos de
VS Code, creá `app.py` y `README.md` si todavía no existen. En esta carpeta ya
están creados: `app.py` contiene un ejemplo de uso de `requests`, y este archivo
es el README.

### 3. Crear y seleccionar `.venv` en VS Code

Desde la terminal abierta en la carpeta del proyecto, creá el entorno virtual:

```powershell
py -m venv .venv
```

Si el comando `py` no está disponible pero `python` sí, usá `python -m venv .venv`.

En VS Code, abrí la paleta de comandos con `Ctrl+Shift+P`, elegí **Python:
Select Interpreter** y seleccioná el intérprete ubicado en `.venv`. En Windows
la ruta suele ser `.venv\Scripts\python.exe`. Si no aparece, cerrá y volvé a
abrir la paleta después de crear el entorno.

### 4. Instalar una biblioteca y registrar las dependencias

Con `.venv` seleccionado, instalá `requests` y guardá las dependencias del
entorno en `requirements.txt`:

```powershell
python -m pip install requests
python -m pip freeze > requirements.txt
```

Probá el programa:

```powershell
python app.py
```

Deberías ver un mensaje indicando que el entorno está listo y la versión de
`requests`. Para instalar más adelante las dependencias registradas, usá:

```powershell
python -m pip install -r requirements.txt
```

### 5. Revisar el estado de Git y registrar un commit

Revisá qué archivos detecta Git:

```powershell
git status
```

Si el proyecto todavía no forma parte de un repositorio, inicializalo una sola
vez con `git init`. Después, desde la carpeta del proyecto, agregá sus archivos
y creá el commit:

```powershell
git add .
git status
git commit -m "Crear proyecto de la clase 2"
```

Antes del commit, verificá con `git status` que `.venv/` no aparezca entre los
archivos preparados. En este material, la carpeta `Clase_2` ya está dentro de
un repositorio Git existente: no ejecutes `git init` dentro de ella. El primer
commit corresponde a un repositorio nuevo; en uno existente, registrá tus
cambios con un commit nuevo.