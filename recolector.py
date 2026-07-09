import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def extraer_resultados_reales():
    print("Iniciando extracción con URLs oficiales...")
    
    # Usamos un "disfraz" de navegador real para que los portales no nos bloqueen la conexión
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    nuevos_resultados = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    # Tus enlaces oficiales
    fuentes = [
        {"nombre": "Loteria del Valle", "url": "https://loteriadelvalle.com/resultado_v2/vistas/tabla.php"},
        {"nombre": "Chontico Dia", "url": "https://www.colombia.com/loterias/chontico-dia"},
        {"nombre": "Chontico Noche", "url": "https://www.colombia.com/loterias/chontico-noche"}
    ]

    for fuente in fuentes:
        try:
            print(f"Conectando a: {fuente['nombre']}...")
            respuesta = requests.get(fuente['url'], headers=headers, timeout=15)
            respuesta.raise_for_status()
            soup = BeautifulSoup(respuesta.text, 'html.parser')

            numero_ganador = None
            
            # Lógica de escaneo: Buscamos textos en negrita, celdas o títulos
            etiquetas_candidatas = soup.find_all(['span', 'div', 'td', 'strong', 'b', 'h1', 'h2'])
            
            for etiqueta in etiquetas_candidatas:
                texto = etiqueta.get_text().strip()
                
                # Validamos matemáticamente: Debe tener 4 caracteres, ser puros números y no ser un año (ej. 2026)
                if len(texto) == 4 and texto.isdigit() and texto not in ["2024", "2025", "2026"]:
                    numero_ganador = texto
                    break # El primer número de 4 cifras que aparece suele ser el premio mayor

            if numero_ganador:
                nuevos_resultados.append({
                    "loteriaNombre": fuente['nombre'],
                    "fecha": fecha_hoy,
                    "numerosPrincipales": numero_ganador,
                    "numeroEspecial": None
                })
                print(f"¡Éxito! -> {fuente['nombre']}: {numero_ganador}")
            else:
                print(f"Fallo -> No se encontró el número ganador en la estructura de {fuente['nombre']}")

        except Exception as e:
            print(f"Error de red procesando {fuente['nombre']}: {e}")

    return nuevos_resultados

def guardar_resultados(nuevos_datos):
    archivo_json = 'sorteos.json'
    
    # 1. Leer los datos que ya tenemos en GitHub
    if os.path.exists(archivo_json):
        with open(archivo_json, 'r', encoding='utf-8') as f:
            try:
                datos_actuales = json.load(f)
            except json.JSONDecodeError:
                datos_actuales = []
    else:
        datos_actuales = []

    # 2. Filtrar para no guardar el sorteo de hoy dos veces
    fechas_existentes = [(s['loteriaNombre'], s['fecha']) for s in datos_actuales]
    
    agregados = 0
    for sorteo in nuevos_datos:
        if (sorteo['loteriaNombre'], sorteo['fecha']) not in fechas_existentes:
            datos_actuales.append(sorteo)
            agregados += 1

    # 3. Guardar el archivo limpio y actualizado
    if agregados > 0:
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(datos_actuales, f, indent=2)
        print(f"Tarea completada: {agregados} sorteos nuevos inyectados a la base de datos.")
    else:
        print("Tarea completada: Los datos ya estaban actualizados (No hay sorteos nuevos).")

if __name__ == "__main__":
    datos_extraidos = extraer_resultados_reales()
    guardar_resultados(datos_extraidos)
