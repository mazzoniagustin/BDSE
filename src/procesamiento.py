from pathlib import Path
import csv
from constantes import DATA_OUT_PATH, PROCESSED_DATA_PATH


"""def load_files (type):
    
    data = []
    
    column = []
    
    if not (DATA_PATH.exists()): # Si no existe, no crashea.
        print(f'La carpeta {DATA_PATH} no existe. Verificá la estructura del proyecto.') 
        return data, column
        
    for archive in DATA_PATH.glob(f"*{type}*.txt"):
        
        with archive.open(encoding="utf-8") as f:
            lect = csv.DictReader(f,delimiter=";")
            
            if not column:
                column.extend(lect.fieldnames)
                
            for row in lect:
                data.append(row)
                
    return data, column"""     # La unificación de los dataset's se lleva a cabo en FUNCIONALIDAD.


def transformar_ch04_str(valor):
    """
    Transforma el valor numérico del género a su representación en texto.

    Parameters
    ----------
    valor : str
        Código numérico del género ('1' para masculino, '2' para femenino).

    Returns
    -------
    str
        "Masculino", "Femenino" o "Desconocido" según el valor recibido.
    """
    
    if (valor == "1"):
        return "Masculino"
    
    elif valor == "2":
        return "Femenino"
    else:
        return "Desconocido"


def transformar_nivel_ed_str(value): 
    """
    Transforma el valor numérico del nivel educativo a su descripción en texto.

    Parameters
    ----------
    value : str
        Código numérico del nivel educativo.

    Returns
    -------
    str
        Descripción textual del nivel educativo.
    """
    
    match value:
        case "1":
            return "Primario incompleto."
        case "2":
            return "Primario completo."
        case "3":
            return "Secundario incompleto."
        case "4":
            return "Secundario completo."
        case "5" | "6":
            return "Superior o universitario."
        case "7" | "9":
            return ("Sin información.")


def transformar_condicion_laboral(est_valor, ocup_valor):
    """
    Transforma los códigos numéricos del estado y categoría ocupacional
    en una descripción del estado laboral.

    Parameters
    ----------
    est_valor : str or None
        Código del estado laboral.
    ocup_valor : str or None
        Código de la categoría ocupacional.

    Returns
    -------
    str or None
        Descripción del estado laboral o None si falta información.
    """
    
    sin_valor = [None, ""]
    
    if est_valor in sin_valor or ocup_valor in sin_valor:
        return None
    else:
        if est_valor == "1":
            if ocup_valor in ("1", "2"):
                return "Ocupado Autónomo."
            if ocup_valor in ("3", "4", "9"):
                return "Ocupado dependiente."
        if est_valor == "2":
            return "Desocupado."
        if est_valor == "3":
            return "Inactivo."
        if est_valor == "4":
            return "Fuera de categoría/Sin información."
    

def clasificar_universitario (edad, nivel_ed):
    """
    Clasifica si una persona mayor de edad completó estudios universitarios.

    Parameters
    ----------
    edad : str or int
        Edad de la persona.
    nivel_ed : str
        Código del nivel educativo.

    Returns
    -------
    str
        "1" si completó estudios universitarios y es mayor de edad,
        "2" si es menor de edad,
        "0" en otros casos o si hay error en los datos.
    """
    try:
        if (int(edad) < 18):
            return "2"
        elif nivel_ed == "6":
            return "1"
        else:
            return "0"
    except (ValueError, TypeError):
        return "0"


def clasificar_tipo_hogar (personas):
    """
    Clasifica el tipo de hogar según la cantidad de personas que viven en él.

    Parameters
    ----------
    personas : str or int
        Número de personas en el hogar.

    Returns
    -------
    str
        Tipo de hogar: "Unipersonal", "Nuclear", "Extendido" o "Desconocido" si hay error.
    """

    try:
        personas = int(personas)
        if personas == 1:
            return "Unipersonal."
        elif 2 <= personas <= 4:
            return "Nuclear."
        else:
            return "Extendido."
    except (ValueError, TypeError):
        return "Desconocido"


def clasificar_material_techumbre(valor):
    """
    Transforma el código numérico del material del techo en su categoría descriptiva.

    Parameters
    ----------
    valor : str or int
        Código del material del techo.

    Returns
    -------
    str
        Categoría del material del techo: "Material Precario", "Material Durable",
        "No aplica" o "N/S".
    """
    
    valor = str(valor).strip()
    match valor:
        case "5" | "6" | "7":
            return "Material Precario"
        case "1" | "2" | "3" | "4":
            return "Material Durable"
        case "9":
            return "No aplica"
        case "_":
            return "N/S."


def densidad_hogar(habitaciones, personas):
    """
    Calcula la densidad del hogar como personas por habitación
    y la clasifica en categorías de densidad.

    Parameters
    ----------
    habitaciones : str or int
        Número de habitaciones del hogar.
    personas : str or int
        Número de personas en el hogar.

    Returns
    -------
    str
        Categoría de densidad: "Bajo", "Medio", "Alto" o mensaje de error si los datos no son válidos.
    """
    
    try:
        personas = int(personas)
        habitaciones = int(habitaciones)

        densidad = personas / habitaciones

        if densidad < 1:
            return "Bajo"
        elif densidad <= 2:
            return "Medio"
        else:
            return "Alto"
        
    except (ValueError, ZeroDivisionError, TypeError):
        return "Error al procesar los datos."



def condicion_habitabilidad (agua, ori_agua, banio, ubi_banio, drenaje, techo):
    """
    Calcula la condicion de habitabilidad entre las categorias de: Insuficiente, Regular, Saludable y Buena.

    Parameters
    ----------
    agua : str
        Código del suministro de agua.
    ori_agua : str
        Origen del agua.
    banio : str
        Código del tipo de baño.
    ubi_banio : str
        Ubicación del baño.
    drenaje : str
        Código del sistema de drenaje.
    techo : str
        Categoría del material del techo.

    Returns
    -------
    str
        Condición de habitabilidad: "Insuficiente", "Regular", "Saludable", "Buena" o "Desconocido".
    """
    
    try:
        if agua == '3' or techo == 'No aplica.':
            return 'Insuficiente'
        elif agua == '2':
            if banio == '2':
                return 'Insuficiente'
            if drenaje == '4' or ubi_banio == '3' or ori_agua == '4':
                return 'Insuficiente'
            elif ubi_banio == '2' or ori_agua == '3':
                return 'Regular'
            else:
                return 'Saludable'
        else:
            if techo == 'Material Durable':
                if drenaje == '4' or ubi_banio == '3' or ori_agua == '4':
                    return 'Regular'
                elif ubi_banio == '2' or ori_agua == '3':
                    return 'Saludable'
                else:
                    return 'Buena'
            else:
                return 'Regular'
    except Exception:
        return 'Desconocido'


def procesar_individuos(ind):
    """
    Procesa todos los individuos unificados, creando las nuevas columnas con los valores transformados.

    Parameters
    ----------
    ind : list of dict
        Lista de diccionarios representando individuos.
    """
    
    for row in ind:
        row["CH04_str"] = transformar_ch04_str(row["CH04"])
        row["NIVEL_ED_str"] = transformar_nivel_ed_str(row["NIVEL_ED"])
        row["CONDICION_LABORAL"] = transformar_condicion_laboral(row["ESTADO"], row["CAT_OCUP"])
        row["UNIVERSITARIO"] = clasificar_universitario(row["CH06"], row["NIVEL_ED"])


def procesar_hogares(hog):
    """
    Procesa todos los hogares unificados, creando las nuevas columnas con los valores transformados.

    Parameters
    ----------
    hog : list of dict
        Lista de diccionarios representando hogares.
    """
    
    for row in hog:
        row["TIPO_HOGAR"] = clasificar_tipo_hogar(row["IX_TOT"])
        row["MATERIAL_TECHUMBRE"] = clasificar_material_techumbre(row["V4"])
        row["DENSIDAD_HOGAR"] = densidad_hogar(row['IV2'], row['IX_TOT'])
        row["CONDICION_DE_HABITABILIDAD"] = condicion_habitabilidad (
            row['IV6'], row['IV7'], row['IV8'], row['IV9'], row['IV11'], row["MATERIAL_TECHUMBRE"]
        )


def procesar_data(indicator=None):
    """
    Esta función procesa todos los datos unificados en bruto y crea un nuevo archivo CSV 
    con las nuevas columnas en la carpeta processed_data.

    Parameters
    ----------
    indicator : str, optional
        Indicador para seleccionar tipo de datos a procesar:
        'I' o 'i' para individuos, 'H' o 'h' para hogares.

    -----
    Verifica la existencia de archivos y directorios necesarios, maneja errores
    comunes y escribe el archivo procesado en la carpeta correspondiente.
    """
    indicadores  = ['I','H','i','h']
    
    
    if indicator not in indicadores:
        print("Ingrese un indicador o ingrese uno adecuado.")
        return
    else:
        try:
            nombre = "individual" if indicator.upper() == 'I' else 'hogar'
    
            entrada_csv = DATA_OUT_PATH / f'usu_{nombre}.csv'
            procesado_csv = PROCESSED_DATA_PATH / f'{nombre}_procesado.csv'
    
            if not (PROCESSED_DATA_PATH.exists()):
                print(f'La carpeta {PROCESSED_DATA_PATH} no existe. Verificá la estructura del proyecto.')
                return
    
            if not (entrada_csv.exists()):
                print(f'El archivo no se encontró. Unifique los datasets primero.')
                return
    
            with entrada_csv.open("r",encoding='utf-8') as entrada:
                csv_reader = csv.DictReader(entrada,delimiter=';')
                data = list(csv_reader)
                columnas = csv_reader.fieldnames.copy()
        
            if indicator.upper() == "I":
                procesar_individuos(data)
                nuevas_columnas = ["CH04_str", "NIVEL_ED_str", "CONDICION_LABORAL", "UNIVERSITARIO"]
            else:
                procesar_hogares(data)
                nuevas_columnas = ["TIPO_HOGAR","MATERIAL_TECHUMBRE","DENSIDAD_HOGAR","CONDICION_DE_HABITABILIDAD"]
    
            for col in nuevas_columnas:
                if col not in columnas:
                    columnas.append(col)
        
            with procesado_csv.open("w",newline="",encoding="utf-8") as procesado:
                csv_writer = csv.DictWriter(procesado,fieldnames=columnas,delimiter=";")
                csv_writer.writeheader()
                for row in data:
                    clean_row = {col: row.get(col, "") for col in columnas}
                    csv_writer.writerow(clean_row)
        except Exception as e: #  Por ejemplo, cuando se corta la creacion del dataset(no hay permisos de escritura).
            print(F'Error al procesar los datos. {e}')