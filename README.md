# Generador de Plantillas de Calendario

Un script en Python para generar calendarios mensuales clásicos en español y exportarlos como imágenes PNG de alta resolución (300 DPI, tamaño A4 apaisado), ideales para imprimir.

Es un script/prueba de concepto para ayudar a un compañero que trabaja en una imprenta

## Requisitos

- Python 3
- Paquetes listados en `requirements.txt` (`playwright`, `jinja2`)

## Instalación

1. Crea un entorno virtual e instálalo:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Uso

Ejecuta el script proporcionando el año y el mes:

```bash
python calendar_generator.py 2026 10
```

Esto generará un archivo llamado `calendario_octubre_2026.png` en el directorio actual.

También puedes especificar el nombre del archivo de salida:
```bash
python calendar_generator.py 2026 10 --output mi_calendario.png
```
