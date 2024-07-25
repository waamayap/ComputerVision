import json
 #
    #  Abrir el archivo JSON y cargar los datos
def extract_info_from_json(json_path):
   
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    # Inicializar variables para almacenar la información extraída
    nro_matricula = ""        # Almacena el número de matrícula
    fecha_impresion = ""      # Almacena la fecha de impresión
    departamento = ""         # Almacena el nombre del departamento
    municipio = ""            # Almacena el nombre del municipio
    localidad = ""            # Almacena el nombre de la localidad (vereda)
    estado_folio = ""         # Almacena el estado del folio

    # Recorrer los bloques del JSON para encontrar los valores requeridos
    for block in data['Blocks']:
        if block['BlockType'] == 'LINE':
            text = block['Text']  # Obtener el texto del bloque
            # Buscar y extraer el número de matrícula
            if "Nro Matrícula:" in text:
                nro_matricula = text.split("Nro Matrícula:")[1].strip()
            # Buscar y extraer la fecha de impresión
            elif "Impreso el" in text:
                fecha_impresion = text.split("Impreso el")[1].split(" a las")[0].strip()
            # Buscar y extraer la información de ubicación
            elif "DEPTO:" in text:
                parts = text.split()  # Dividir el texto en palabras
                # Extraer el departamento, municipio y localidad (vereda)
                departamento = parts[parts.index("DEPTO:") + 1]
                municipio = parts[parts.index("MUNICIPIO:") + 1]
                localidad = parts[parts.index("VEREDA:") + 1] if "VEREDA:" in parts else ""
            # Buscar y extraer el estado del folio
            elif "ESTADO DEL FOLIO:" in text:
                estado_folio = text.split("ESTADO DEL FOLIO:")[1].strip()
    
    # Formatear la fecha de impresión al formato AAAA-MM-DD
    fecha_impresion = format_date(fecha_impresion)
    
    # Retornar un diccionario con los datos extraídos
    return {
        "Nro Matrícula": nro_matricula,
        "Fecha de Impresión": fecha_impresion,
        "Departamento": departamento,
        "Municipio": municipio,
        "Localidad (vereda)": localidad,
        "Estado del Folio": estado_folio
    }

def format_date(date_str):
    # Limpiar la cadena de fecha eliminando " de "
    date_str = date_str.replace(" de ", " ")
    parts = date_str.split()
    # Verificar que el formato de la fecha sea correcto
    if len(parts) == 3:
        day, month, year = parts
    else:
        raise ValueError(f"Formato de fecha no válido: {date_str}")
    
    # Diccionario para convertir los nombres de los meses a números
    months = {
        "Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04", 
        "Mayo": "05", "Junio": "06", "Julio": "07", "Agosto": "08", 
        "Septiembre": "09", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"
    }

    # Asegurar que el día tenga dos dígitos
    day = day.zfill(2)
    # Obtener el número del mes
    month = months[month]
    # Retornar la fecha en formato AAAA-MM-DD
    return f"{year}-{month}-{day}"


json_path = '001-1007202-220301269555588250_pag1.json'  # Ruta del archivo JSON
info = extract_info_from_json(json_path)  # Extraer información del JSON
print(info)  # Imprimir la información extraída
