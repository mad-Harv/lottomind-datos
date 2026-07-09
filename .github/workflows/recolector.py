import json
import datetime
import os

# Aquí es donde el script descargará los datos reales de internet (Web Scraping o APIs)
# Por ahora, simularemos que descargó el sorteo de hoy para mantener la estructura

fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")

nuevos_sorteos = [
    {
        "loteriaNombre": "Chontico Dia",
        "fecha": fecha_hoy,
        "numerosPrincipales": "1234", # Aquí iría la lógica para extraer el real
        "numeroEspecial": None
    }
]

# Leer el archivo existente
archivo_json = 'sorteos.json'
if os.path.exists(archivo_json):
    with open(archivo_json, 'r', encoding='utf-8') as f:
        datos_actuales = json.load(f)
else:
    datos_actuales = []

# Evitar duplicados y agregar los nuevos
fechas_existentes = [(s['loteriaNombre'], s['fecha']) for s in datos_actuales]

for sorteo in nuevos_sorteos:
    if (sorteo['loteriaNombre'], sorteo['fecha']) not in fechas_existentes:
        datos_actuales.append(sorteo)

# Guardar el archivo actualizado
with open(archivo_json, 'w', encoding='utf-8') as f:
    json.dump(datos_actuales, f, indent=2)

print("Datos actualizados correctamente.")
