"""Comprobación mínima de la dependencia instalada en el entorno virtual."""

import requests


def main() -> None:
    print(f"Entorno listo. requests {requests.__version__}")


if __name__ == "__main__":
    main()