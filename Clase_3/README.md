# Clase 3: Git y repositorios

Esta actividad practica el flujo básico de cambios en Git y cómo describir un
problema concreto en un repositorio.

## Práctica

1. Abrí una terminal en la raíz de este repositorio y ejecutá `git status`.
2. Elegí un archivo de texto de una clase y hacé un cambio pequeño y útil.
3. Volvé a ejecutar `git status` y observá qué cambió.
4. Revisá el diff antes de preparar el cambio:

   ```powershell
   git diff
   ```

5. Agregá solo el archivo que modificaste, revisá el área de preparación y
   creá un commit:

   ```powershell
   git add ruta\al\archivo
   git diff --cached
   git commit -m "Documentar una actividad"
   ```

6. Confirmá el resultado con `git status` y `git log -1 --oneline`.

No agregues tokens, entornos virtuales, archivos temporales ni cambios ajenos a
la actividad. Si encontrás un problema en otro repositorio, describí los pasos
para observarlo, el resultado esperado, el resultado real y una sugerencia
acotada; no modifiques el repositorio de otra persona sin autorización.

## Ticket de salida

Respondé con tus palabras:

- ¿Qué diferencia hay entre el directorio de trabajo y los cambios preparados?
- ¿Qué información aporta el mensaje de un commit?
- ¿Qué revisarías antes de subir un cambio al repositorio remoto?
