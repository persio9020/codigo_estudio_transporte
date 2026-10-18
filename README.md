# Estudio de caso: IA para el transporte público de Bogotá

## Advertencia metodológica
El código es un prototipo académico. No incluye datos reales recolectados ni afirma que se ejecutó contra X/Twitter. Para el informe se usan datos sintéticos únicamente para demostrar el flujo. Antes de recolectar datos de plataformas, revise términos de servicio, permisos, límites técnicos y normas de protección de datos.

## Entorno
Python 3.11 recomendado.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download es_core_news_sm
pytest -q
```

## Ejecución
```bash
python collect.py --html data/demo.html --output data/publicaciones.json
python analyze.py --input data/publicaciones.json --output data/analisis.json
python propose.py
```
`collect.py` también admite `--url` para páginas de acceso público cuyo uso automatizado esté permitido.

## Contenido
- `collect.py`: recolección con Selenium.
- `analyze.py`: clasificación léxica de temas y extracción de lugares con spaCy.
- `propose.py`: recomendaciones explicables sujetas a validación humana.
- `test_propose.py`: pruebas PyTest e Hypothesis.
- `data/demo.html`: contenido ficticio para probar la tubería sin acceder a redes sociales.
