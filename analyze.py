"""Análisis NLP y conteo de temas; no interpreta el conteo como demanda real."""
import re
from collections import Counter
import spacy

TOPIC_TERMS = {
    "demoras": ["demora", "tarde", "espera", "retraso", "demorado", "frecuencia"],
    "congestion": ["congestión", "trancón", "tráfico", "atascado", "colapsado"],
    "ocupacion": ["lleno", "llena", "abarrotado", "ocupación", "aforo"],
    "seguridad": ["inseguro", "robo", "hurto", "acoso", "seguridad"],
    "informacion": ["información", "aviso", "ruta", "horario", "desvío"]
}

def load_model():
    try:
        return spacy.load("es_core_news_sm")
    except OSError as exc:
        raise RuntimeError(
            "Falta el modelo español. Ejecute: python -m spacy download es_core_news_sm"
        ) from exc

def normalize(text):
    return re.sub(r"\s+", " ", str(text)).strip().lower()

def analyze_posts(posts, nlp=None):
    nlp = nlp or load_model()
    result = Counter()
    place_mentions = Counter()
    for post in posts:
        clean = normalize(post)
        if not clean:
            continue
        for topic, terms in TOPIC_TERMS.items():
            if any(re.search(r"\b" + re.escape(term) + r"\w*\b", clean) for term in terms):
                result[topic] += 1
        doc = nlp(post)
        for ent in doc.ents:
            if ent.label_ in {"LOC", "GPE", "FAC"}:
                place_mentions[ent.text] += 1
    return {"temas": dict(result), "lugares": dict(place_mentions), "total": len([p for p in posts if normalize(p)])}

if __name__ == "__main__":
    import argparse, json
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/publicaciones.json")
    parser.add_argument("--output", default="data/analisis.json")
    args = parser.parse_args()
    posts = json.loads(Path(args.input).read_text(encoding="utf-8"))
    report = analyze_posts(posts)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
