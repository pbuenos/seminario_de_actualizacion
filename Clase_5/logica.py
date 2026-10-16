def crear_saludo(nombre: str, estilo: str) -> str:
    nombre = nombre.strip()
    if not nombre:
        return "Escribí tu nombre para crear un saludo."

    if estilo == "Formal":
        return f"Buenos días, {nombre}. ¿Cómo está?"
    return f"¡Hola, {nombre}! ¿Cómo estás?"
