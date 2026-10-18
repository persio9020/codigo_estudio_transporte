"""Generación de recomendaciones transparentes a partir de menciones por tema."""
def propose_optimizations(analysis, threshold=5):
    recommendations = []
    topics = analysis.get("temas", {})
    mapping = {
        "demoras": "Evaluar intervalos y regularidad del servicio en franjas reportadas con demoras.",
        "congestion": "Contrastar reportes de congestión con datos operacionales antes de ajustar tiempos.",
        "ocupacion": "Revisar demanda y capacidad por franja; considerar refuerzos donde los datos oficiales lo justifiquen.",
        "seguridad": "Remitir patrones agregados a los equipos responsables de seguridad, sin publicar datos personales.",
        "informacion": "Mejorar avisos sobre rutas, horarios y desvíos en canales oficiales."
    }
    for topic, count in topics.items():
        if count >= threshold and topic in mapping:
            recommendations.append({
                "tema": topic, "menciones": count, "propuesta": mapping[topic],
                "validacion_humana_requerida": True
            })
    return recommendations

if __name__ == "__main__":
    import json
    from pathlib import Path
    analysis = json.loads(Path("data/analisis.json").read_text(encoding="utf-8"))
    recs = propose_optimizations(analysis)
    Path("data/recomendaciones.json").write_text(json.dumps(recs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(recs, ensure_ascii=False, indent=2))
