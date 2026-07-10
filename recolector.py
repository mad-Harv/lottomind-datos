import json
from collections import Counter

# Supongamos que tu script ya guardó los sorteos en 'sorteos_historicos.json'
def realizar_analisis_estadistico():
    try:
        with open('sorteos_historicos.json', 'r') as file:
            datos_crudos = json.load(file)
            
        estadisticas_completas = {}
        
        # Iteramos sobre cada lotería en tu base de datos
        for loteria, sorteos in datos_crudos.items():
            todos_los_numeros = []
            
            # Extraemos todos los números principales que han caído
            for sorteo in sorteos:
                # Asumiendo que sorteo['numeros'] es un string como "12,29,34,39,44" o "4921"
                if ',' in sorteo['numeros']:
                    numeros_separados = sorteo['numeros'].split(',')
                    todos_los_numeros.extend(numeros_separados)
                else:
                    # Para loterías de 4 dígitos unidos (ej. Chontico o Valle)
                    todos_los_numeros.extend(list(sorteo['numeros']))
                    
            # Análisis Matemático: Frecuencias Absolutas
            conteo = Counter(todos_los_numeros)
            
            # Ordenar de mayor a menor frecuencia
            numeros_ordenados = conteo.most_common()
            
            if numeros_ordenados:
                # Separamos los 5 más calientes y los 5 más fríos
                calientes = numeros_ordenados[:5]
                frios = numeros_ordenados[-5:]
                
                estadisticas_completas[loteria] = {
                    "total_sorteos_analizados": len(sorteos),
                    "numeros_calientes": [{"numero": num, "frecuencia": freq} for num, freq in calientes],
                    "numeros_frios": [{"numero": num, "frecuencia": freq} for num, freq in frios]
                }
                
        # Guardar el análisis profundo en un nuevo archivo
        with open('estadisticas.json', 'w') as outfile:
            json.dump(estadisticas_completas, outfile, indent=4)
            
        print("Análisis estadístico completado y guardado en estadisticas.json")
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo de sorteos históricos para analizar.")

# Ejecutar la función
realizar_analisis_estadistico()
