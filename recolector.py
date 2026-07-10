import re
import json

def procesar_resultados_play4(texto_crudo_web):
    # Esta fórmula busca en el texto el patrón de fecha y los resultados de Midday y Evening
    patron = r"(\d{1,2}/\d{1,2}/\d{4})\s*\|\s*(\d-\d-\d-\d).*?\|\s*(\d-\d-\d-\d)"
    coincidencias = re.findall(patron, texto_crudo_web)

    sorteos_procesados = []
    
    for fecha, midday, evening in coincidencias:
        # Reemplazar los guiones por comas (ej. "5-5-5-7" pasa a ser "5,5,5,7")
        num_midday = midday.replace('-', ',')
        num_evening = evening.replace('-', ',')

        # Ajustar la fecha al formato YYYY-MM-DD requerido por Room
        mes, dia, anio = fecha.split('/')
        fecha_formateada = f"{anio}-{mes.zfill(2)}-{dia.zfill(2)}"

        # Inyectar el sorteo de Mediodía (Midday)
        sorteos_procesados.append({
            "id": f"PLAY4_MIDDAY-{fecha_formateada}",
            "lotteryType": "PLAY4",
            "country": "USA",
            "drawDate": fecha_formateada,
            "numbers": num_midday
        })
        
        # Inyectar el sorteo de Noche (Evening)
        sorteos_procesados.append({
            "id": f"PLAY4_EVENING-{fecha_formateada}",
            "lotteryType": "PLAY4",
            "country": "USA",
            "drawDate": fecha_formateada,
            "numbers": num_evening
        })

    # Aquí el script debe guardar 'sorteos_procesados' en tu archivo sorteos.json
    return sorteos_procesados

# (Asegúrate de llamar a esta función cuando tu recolector descargue la página de Play 4)
