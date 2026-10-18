"""
Recolección demostrativa de publicaciones sobre transporte público.
Importante: el anexo propone Selenium sobre Twitter/X. La estructura actual de X
puede requerir autenticación y sus condiciones pueden restringir la automatización.
Para una ejecución reproducible, el programa permite procesar HTML local de prueba.
"""
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def setup_selenium(chromedriver_path=None):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1400,1000")
    if chromedriver_path:
        service = Service(chromedriver_path)
        return webdriver.Chrome(service=service, options=options)
    return webdriver.Chrome(options=options)  # Selenium Manager puede resolver driver

def collect_from_url(driver, url):
    driver.get(url)
    articles = driver.find_elements(By.CSS_SELECTOR, "article")
    return [a.text.strip() for a in articles if a.text.strip()]

def collect_from_local_html(driver, html_path):
    driver.get(Path(html_path).resolve().as_uri())
    articles = driver.find_elements(By.CSS_SELECTOR, "article")
    return [a.text.strip() for a in articles if a.text.strip()]

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL pública permitida para consulta")
    parser.add_argument("--html", help="Ruta a archivo HTML local de prueba")
    parser.add_argument("--driver", help="Ruta opcional a chromedriver")
    parser.add_argument("--output", default="data/publicaciones.json")
    args = parser.parse_args()
    if not args.url and not args.html:
        parser.error("Indique --url o --html")
    driver = setup_selenium(args.driver)
    try:
        data = collect_from_url(driver, args.url) if args.url else collect_from_local_html(driver, args.html)
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Publicaciones recolectadas: {len(data)}. Archivo: {args.output}")
    finally:
        driver.quit()
