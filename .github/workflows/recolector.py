import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def extraer_chontico_y_valle():
    print("Iniciando extracción de Chontico y Valle...")
    
    # Usaremos un portal genérico de resultados como ejemplo (debes ajustar la URL al portal que elijas)
    url = "https://www.loteriasdecolombia.com/resultados"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    nuevos_resultados = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    try:
        respuesta = requests.get(url, headers=headers)
        respuesta.raise_for_status() # Verifica que la conexión fue exitosa
        soup = BeautifulSoup(respuesta.text, 'html.parser')

        # === DICCIONARIO DE LOTERÍAS A BUSCAR ===
        # Claves: Nombres exactos en tu app | Valores: Texto que buscamos en la web
        loterias_objetivo = {
            "Chontico Dia": "chontico dia",
            "Chontico Noche": "chontico noche",
            "Loteria del Valle": "valle"
        }

        # Buscamos todos los bloques de resultados en la página
        # Nota: 'resultado-item' y 'numero-ganador' son clases de ejemplo. 
        # Debes inspeccionar la página web real para poner las clases correctas.
        bloques_sorteos = soup.find_all('div', class_='resultado-item')

        for bloque in bloques_sorteos:
            titulo_web = bloque.find('h2').text.lower() if bloque.find('h2') else ""
            
            for nombre_app, nombre_busqueda in loterias_objetivo.items():
                if nombre_busqueda in titulo_web:
                    # Extraemos el número de 4 cifras
                    # Suponemos que está en un <span> con la clase 'numero-ganador'
                    numero_str = bloque.find('span', class_='numero-ganador')
                    
                    if numero_str:
                        numero_limpio = numero_str.text.strip()
                        
                        # Verificamos que realmente sean 4 dígitos
                        if len(numero_limpio) == 4 and numero_limpio.isdigit():
                            nuevos_resultados.append({
                                "loteriaNombre": nombre_app,
                                "fecha": fecha_hoy,
                                "numerosPrincipales": numero_limpio,
                                "numeroEspecial": None
                            })
                            print(f"Éxito: {nombre_app} - Resultado: {numero_limpio}")

    except Exception as e:
        print(f"Error al extraer datos de Colombia: {e}")

    return nuevos_resultados

def guardar_resultados(nuevos_datos):
    archivo_json = 'sorteos.json'
    
    # 1. Leer datos existentes
    if os.path.exists(archivo_json):
        with open(archivo_json, 'r', encoding='utf-8') as f:
            try:
                datos_actuales = json.load(f)
            except json.JSONDecodeError:
                datos_actuales = []
    else:
        datos_actuales = []

    # 2. Filtrar duplicados (misma lotería, misma fecha)
    fechas_existentes = [(s['loteriaNombre'], s['fecha']) for s in datos_actuales]
    
    agregados = 0
    for sorteo in nuevos_datos:
        if (sorteo['loteriaNombre'], sorteo['fecha']) not in fechas_existentes:
            datos_actuales.append(sorteo)
            agregados += 1

    # 3. Guardar el archivo actualizado
    if agregados > 0:
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(datos_actuales, f, indent=2)
        print(f"Se agregaron {agregados} sorteos nuevos al archivo maestro.")
    else:
        print("No hay sorteos nuevos para agregar hoy.")

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    datos_colombia = extraer_chontico_y_valle()
    
    # Aquí puedes sumar las listas de Estados Unidos cuando las tengas
    # datos_totales = datos_colombia + datos_usa
    
    guardar_resultados(datos_colombia)
