from constantes import DATA_PATH, DATA_OUT_PATH
import csv

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def creacion_datasets (indicador=None):
    """
    Unifica todos los datasets descargados de individuos o hogares en un solo archivo CSV.

    Parámetros:
    -----------
    indicador : str, opcional
        Indicador para seleccionar el tipo de dataset a unir.
        Puede ser:
        - 'I' o 'i' para datasets de individuos.
        - 'H' o 'h' para datasets de hogares.
        Si no se especifica un indicador válido, la función imprime un mensaje y no realiza acción.

    Comportamiento:
    ---------------
    - Verifica que las carpetas de datos (DATA_PATH) y salida (DATA_OUT_PATH) existan.
    - Busca archivos que coincidan con el patrón correspondiente al indicador dado.
    - Concadena todos los archivos encontrados en un único archivo de salida, preservando el encabezado solo una vez.
    - En caso de error al leer algún archivo (no encontrado o sin permisos), imprime un aviso y continúa.
    """
    
    indicadores = ["I","H","i","h"]
    
    if indicador not in indicadores:
        print('Ingrese un indicador/Ingrese un indicador válido.')
        return
    else:
        if not DATA_PATH.exists():
            print(f"La carpeta {DATA_PATH} no existe. Verificá la estructura del proyecto.")
            return

        if not DATA_OUT_PATH.exists():
            print(f"La carpeta {DATA_OUT_PATH} no existe. Verificá la estructura del proyecto.")
            return
    
        nombre_archivo = "usu_individual" if indicador.upper() == "I" else "usu_hogar"
        archivo_salida = DATA_OUT_PATH / f"{nombre_archivo}.csv"
        tiene_encabezado = False

        with archivo_salida.open('w', newline='', encoding='utf-8-sig') as salida:
            writer = csv.writer(salida, delimiter=';')
            for archivo in DATA_PATH.glob('*.txt'):
                if nombre_archivo in archivo.name.lower():
                    try:
                        with archivo.open('r', encoding='utf-8') as f:
                            reader = (csv.reader(f, delimiter=';'))
                            encabezado = next(reader)  # Leer el encabezado del archivo
                            if not tiene_encabezado:
                                writer.writerow(encabezado)
                                tiene_encabezado = True
                            for line in reader:
                                writer.writerow(line)
                    except FileNotFoundError:
                        print(f"Un archivo {archivo} fue eliminado antes de poder leerlo. Se omite.")
                    except PermissionError:
                        print(f"No se tienen permisos para leer el archivo {archivo}. Se omite.") 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#ESTAS FUNCIONES SE USAN EN LOS SIGUIENTES INCISOS

def aglo_dict():
    """
    Devuelve un diccionario que mapea los códigos de aglomerado con sus respectivos nombres.

    Retorna:
    --------
    dict
        Diccionario donde las claves son códigos de aglomerados (str) y los valores son nombres descriptivos (str).
    """
    
    AGLOMERADOS={
        '2': 'Gran La Plata', '3': 'Bahía Blanca-Cerri', '4': 'Gran Rosario',
        '5': 'Gran Santa Fe', '6': 'Gran Paraná', '7': 'Posadas', '8': 'Gran Resistencia',
        '9': 'Comodoro Rivadavia-Rada Tilly', '10': 'Gran Mendoza', '12': 'Corrientes',
        '13': 'Gran Córdoba', '14': 'Concordia', '15': 'Formosa', '17': 'Neuquén-Plottier',
        '18': 'Santiago del Estero-La Banda', '19': 'Jujuy-Palpalá', '20': 'Río Gallegos',
        '22': 'Gran Catamarca', '23': 'Gran Salta', '25': 'La Rioja', '26': 'Gran San Luis',
        '27': 'Gran San Juan', '29': 'Gran Tucumán-Tafí Viejo', '30': 'Santa Rosa-Toay',
        '31': 'Ushuaia-Río Grande', '32': 'Ciudad Autónoma de Buenos Aires',
        '33': 'Partidos del Gran Buenos Aires', '34': 'Mar del Plata', '36': 'Río Cuarto',
        '38': 'San Nicolás-Villa Constitución', '91': 'Rawson-Trelew', '93': 'Viedma-Carmen de Patagones'}
    return AGLOMERADOS


def defaultcantidades():
    """
    Devuelve un diccionario con códigos de aglomerado como claves y valores inicializados para conteos.

    Retorna:
    --------
    dict
        Diccionario con códigos de aglomerado (str) como claves y como valores otro diccionario con la clave 'cant' inicializada en 0.
    """
    
    AGLOMERADOS=['2','3','4','5','6','7','8','9','10','12','13',
        '14','15','17','18','19','20','22','23','25','26','27','29','30','31',
        '32','33','34','36','38','91','93']
    return {x: {'cant': 0} for x in AGLOMERADOS}


def sacar_porcentaje(diccionariocontador):
    """
    Calcula el porcentaje de un subgrupo respecto al total para cada aglomerado en el diccionario dado.

    Parámetros:
    -----------
    diccionariocontador : dict
        Diccionario donde cada clave es un código de aglomerado (str) y el valor es un diccionario
        que contiene al menos las claves 'cant' (total) y 'cantesp' (subgrupo).

    Retorna:
    --------
    list of tuples
        Lista ordenada descendente de tuplas (aglomerado, porcentaje), donde porcentaje es el cálculo 
        de (cantesp / cant) * 100 para cada aglomerado.
    """
    
    resultados = []
    for aglomerado , data  in diccionariocontador.items():
        totaldatos = int(data['cant'])
        totalesp = int(data['cantesp'])
        porcentaje = (totalesp / totaldatos) * 100 if totaldatos > 0 else 0
        resultados.append((aglomerado, porcentaje))
    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# FUNCIONALIDAD PARA STREAMLITS
def calcular_fechas(archivocsv):
    """
    Calcula el año y trimestre mínimo y máximo presentes en un archivo CSV.

    Parámetros:
    archivocsv (str): Ruta al archivo CSV que contiene los datos.

    Salida:
    Retorna una tupla con cuatro valores enteros: (menor_año, menor_trimestre, mayor_año, mayor_trimestre),
    representando el rango de fechas encontradas en el archivo.

    Excepciones:
    FileNotFoundError: Si el archivo CSV no se encuentra.
    Exception: Cubre cualquier otro error inesperado.
    """
    
    menor_anio = float('inf')
    menor_trimestre = float('inf')
    mayor_anio = float('-inf')
    mayor_trimestre = float('-inf')

    try:
        with open(archivocsv, encoding="utf-8") as f:
            next(f)  # Saltar encabezado
            for linea in f:
                columnas = linea.strip().split(";")
                anio = int(columnas[1])
                trimestre = int(columnas[2])
                if anio < menor_anio:
                    menor_anio = anio
                    menor_trimestre = trimestre
                elif anio == menor_anio:
                    menor_trimestre = min(menor_trimestre, trimestre)

                if anio > mayor_anio:
                    mayor_anio = anio
                    mayor_trimestre = trimestre
                elif anio == mayor_anio:
                    mayor_trimestre = max(mayor_trimestre, trimestre)
        return menor_anio, menor_trimestre, mayor_anio, mayor_trimestre
    
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

def calcular_fechas_comparadas(archivocsv_hogar, archivocsv_individual):
    """
    Compara dos archivos (archivo de individuos y hogares) para encontrar la fecha mínima y máxima conjunta.

    Parámetros:
    archivocsv_hogar (str): Ruta al archivo CSV de hogares.
    archivocsv_individual (str): Ruta al archivo CSV de individuos.

    Salida:
    Retorna una tupla con cuatro valores enteros: (menor_año, menor_trimestre, mayor_año, mayor_trimestre),
    que representa las fechas mínimas y máximas combinadas de ambos archivos.

    Excepciones:
    FileNotFoundError: Si alguno de los archivos CSV no se encuentra.
    Exception: Cubre cualquier otro error inesperado.
    """

    fechas_hogar = calcular_fechas(archivocsv_hogar)
    fechas_individual = calcular_fechas(archivocsv_individual)

    # Verificar si alguno devolvió None
    if fechas_hogar is None and fechas_individual is None:
        return None
    elif fechas_hogar is None:
        return fechas_individual
    elif fechas_individual is None:
        return fechas_hogar

    # Mínimo
    menor_anio = min(fechas_hogar[0], fechas_individual[0])
    if menor_anio == fechas_hogar[0]:
        menor_trimestre = min(
            fechas_hogar[1],
            fechas_individual[1] if menor_anio == fechas_individual[0] else 999
        )
    else:
        menor_trimestre = min(
            fechas_individual[1],
            fechas_hogar[1] if menor_anio == fechas_hogar[0] else 999
        )

    # Máximo
    mayor_anio = max(fechas_hogar[2], fechas_individual[2])
    if mayor_anio == fechas_hogar[2]:
        mayor_trimestre = max(
            fechas_hogar[3],
            fechas_individual[3] if mayor_anio == fechas_individual[2] else -1
        )
    else:
        mayor_trimestre = max(
            fechas_individual[3],
            fechas_hogar[3] if mayor_anio == fechas_hogar[2] else -1
        )

    return menor_anio, menor_trimestre, mayor_anio, mayor_trimestre


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INCISO 1 SECCION B = Imprime año tras año el porcentaje de personas +6 años alfabetizados y analfabetizados.

def porcentaje_alfabetizacion (archivo_csv):
    """
    Calcula e imprime el porcentaje de personas mayores a 6 años que saben y que no saben leer y escribir,
    considerando únicamente los datos del cuarto trimestre de cada año.

    Parámetros:
    archivo_csv (str): Ruta al archivo CSV que contiene los datos de personas.

    Salida:
    Muestra por consola, por cada año presente en el archivo, el porcentaje de personas alfabetizadas
    (que saben leer y escribir) y no alfabetizadas (que no saben leer y escribir), considerando solo
    a las personas mayores de 6 años.

    Excepciones:
    KeyError: Si falta alguna columna esperada en el CSV.
    FileNotFoundError: Si el archivo CSV no se encuentra.
    ValueError: Si los datos esperados como enteros no se pueden convertir.
    Exception: Cubre cualquier otro error inesperado.
    """

    CH09 = 16 # Sabe leer: 1= Sí; 2= No; 3 =Menor de 2 años
    CH06 = 13 # edad
    pondera = 9 # cantidad de personas que contempla
    trimestre = 2 # trimestre del registro
    ANO4 = 1 # año del registro

    datos_por_anio = {}

    try:
        with open(archivo_csv, 'r', encoding='utf-8') as archivo:
            reader = csv.reader(archivo, delimiter=';')
            next(reader)

            for row in reader:
                if (row[trimestre] == "4"):
                    edad = int(row[CH06])
                    if edad > 6:
                        capacidad = row[CH09]
                        anio = row[ANO4]
                        cantidad = int(row[pondera])

                        if anio not in datos_por_anio:
                            datos_por_anio[anio] = {"total": 0, "cumple": 0}

                        datos_por_anio[anio]["total"] += cantidad
                        if capacidad == "1":
                            datos_por_anio[anio]["cumple"] += cantidad

        for anio in sorted(datos_por_anio):
            total = datos_por_anio[anio]["total"]
            capaces = datos_por_anio[anio]["cumple"]
            porcentaje_leen = (capaces / total) * 100
            porcentaje_no_leen = 100 - porcentaje_leen
            print(f"En el año {anio} El porcentaje de personas > 6 años alfabetizadas es: "
                f"{porcentaje_leen:.2f}% / El porcentaje de analfabetizadas: {porcentaje_no_leen:.2f}%")

    except KeyError as e:
        print(f"Error: faltan columnas esperadas en los CSV. Columna faltante: {e}")
    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        print("Error: se esperaba un número pero se recibió otro dato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INCISO 2 SECCION B= Dado un año imprime el porcentaje de inmigrantes que hayan cursado nivel universitario o superior

def porcentaje_inmigrantes_academicos(archivo_csv):
    """
    Imprime el porcentaje de personas inmigrantes que han cursado nivel universitario o superior
    en un año y trimestre ingresados por el usuario.

    Parámetros:
    archivo_csv (str): Ruta al archivo CSV con datos de personas.

    Salida:
    Imprime por consola el porcentaje de inmigrantes con nivel universitario alcanzado
    respecto al total de personas registradas en el período solicitado.

    Excepciones:
    KeyError: Si falta alguna columna esperada.
    FileNotFoundError: Si el archivo CSV no se encuentra.
    ValueError: Si los valores ingresados o leídos no pueden convertirse correctamente a número.
    Exception: Para cualquier otro error inesperado.
    """

    CH12 = 19 # ¿Cuál es el nivel más alto que cursa/ó? = 7 (universitario)
    CH15 = 22 # ¿Dónde nació? = 4 / 5 (fuera del país)  
    pondera = 9 # cantidad de personas que contempla
    trim = 2 # trimestre del registro
    year = 1 # año del registro

    total_personas = 0
    inmigrantes_universitarios = 0
    existe_año_trimestre = False

    try:
        trimestre = input("Ingrese un trimestre: ")
        anio = input("Ingrese un año: ")

        if not trimestre.isdigit() or not anio.isdigit():
            print('Ingrese un valor numerico.')
            return
        
        trimestre = int(trimestre)
        anio = int(anio)
        
        if trimestre not in (1,2,3,4):
            print("El trimestre debe ser un valor entre 1-4")
            return
        
        with open(archivo_csv, 'r', encoding='utf-8') as archivo:
            reader = csv.reader(archivo, delimiter=';')
            next(reader)

            for row in reader:
                if int(row[year]) == anio:
                    if int(row[trim]) == trimestre:
                        existe_año_trimestre = True
                        total_personas += int(row[pondera])
                        if (row[CH12]) >= "7":
                            if row[CH15] in ["4", "5"]:
                                inmigrantes_universitarios += int(row[pondera])

        if not existe_año_trimestre:
            print(f"No se encontraron datos para el año {anio} y trimestre {trimestre}.")
        else:
            if total_personas == 0:
                print("No hay personas ponderadas para esos criterios, no se puede calcular porcentaje.")
            else:
                print(f"En el año {anio}, trimestre numero {trimestre} "
                      f"{(inmigrantes_universitarios / total_personas) * 100}%"
                      " son personas no nacidas en argentina que han cursado nivel universitario o superior.")
                
    except KeyError as e:
        print(f"Error: faltan columnas esperadas en los CSV. Columna faltante: {e}")
    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        print("Error: se esperaba un número pero se recibió otro dato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INCISO 3 SECCION B = Informa el año con menor desocupacion.

def menor_desocupacion_anio_trim(archivo_csv):
    """
    Imprime el año y trimestre con menor cantidad de personas desocupadas registradas.

    Parámetros:
    archivo_csv (str): Ruta al archivo CSV que contiene los registros laborales.

    Salida:
    Muestra por consola el año y trimestre con la menor cantidad de desocupación total.

    Excepciones:
    KeyError: Si falta alguna columna esperada.
    FileNotFoundError: Si no se encuentra el archivo especificado.
    ValueError: Si un dato que debía ser numérico no lo es.
    Exception: Para cualquier otro error inesperado.
    """
    
    condicion_laboral = 179 # Campo de strings: Desocupado.
    pondera = 9 # cantidad de personas que contempla
    trim = 2 # trimestre del registro
    year = 1 # año del registro
    desocupados_por_periodo = {}

    try:
        with open(archivo_csv, 'r', encoding='utf-8') as archivo:
            reader = csv.reader(archivo, delimiter=';')
            next(reader)
            
            for row in reader:
                condicion = row[condicion_laboral].strip()
                if (condicion == "Desocupado."):
                    anio = int(row[year])
                    trimestre = int(row[trim])
                    cantidad = int(row[pondera])
                    clave = (anio,trimestre)

                    if clave not in desocupados_por_periodo:
                        desocupados_por_periodo[clave] = 0
                    desocupados_por_periodo[clave] += cantidad

        anio_min, trim_min = min(desocupados_por_periodo, key= desocupados_por_periodo.get)
        print(f"Menor desocupación: año {anio_min}, trimestre numero {trim_min}.")

    except KeyError as e:
        print(f"Error: faltan columnas esperadas en los CSV. Columna faltante: {e}")
    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        print("Error: se esperaba un número pero se recibió otro dato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INCISO 4 SECCION B= Ranking 5 aglomerados con mas de 2 ocupantes en un hogar con estudios universitarios o superiores

def top_5_aglomerados_universitarios(archivo_csv_hogares, archivo_csv_personas, ok = False):
    """
    Imprime el ranking de los 5 aglomerados con mayor porcentaje de hogares con al menos
    dos personas con estudios universitarios o superiores finalizados.

    Parámetros:
    archivo_csv_hogares (str): Ruta al archivo CSV de hogares.
    archivo_csv_personas (str): Ruta al archivo CSV de personas.

    Salida:
    Muestra en consola el top 5 de aglomerados con mayor porcentaje de hogares que 
    cumplen la condición.

    Excepciones:
    KeyError: Si falta una columna esperada.
    FileNotFoundError: Si alguno de los archivos no existe.
    ValueError: Si un dato numérico no es válido.
    Exception: Para cualquier otro error inesperado.
    """
    
    UNIVERSITARIO = 180 # columna generada en la seccion a, inciso 6 (1: Sí, 0: No, 2: no aplica).
    CODUSU = 0 # codigo de vivienda, apareable con personas
    NRO_HOGAR = 3 # codigo para distinguir hogares
    AGLOMERADO_HOGAR = 7 # codigo de aglomerado
    PONDERA_HOG = 8 # cantidad de personas que contempla
    trim = 2 # trimestre del registro
    year = 1 # año del registro
    anio, trimestre = calcular_fechas(archivo_csv_hogares)[2:] # Obtener el año y trimestre más recientes

    AGLOMERADOS = aglo_dict()
    diccionario_contador = defaultcantidades()

    for valor in diccionario_contador.values():
        valor['cantesp'] = 0  # agregamos campo extra que contabiliza la condicion de recibidos
    try:
        # Leer archivo de personas y agrupar por hogar
        personas_por_hogar = {}
        with open(archivo_csv_personas, 'r', encoding='utf-8') as archivo_personas:
            personas_reader = csv.reader(archivo_personas, delimiter=';')
            next(personas_reader)
            for row in personas_reader:
                if int(row[year]) == anio and int(row[trim]) == trimestre:
                    if row[UNIVERSITARIO] == '1': # si cumple identifica su hogar
                        codusu = row[CODUSU].strip()
                        nro_hogar = row[NRO_HOGAR].strip()
                        hogar_id = (codusu, nro_hogar)

                        if hogar_id not in personas_por_hogar: # se agrega esa persona al hogar en el dict
                            personas_por_hogar[hogar_id] = 0 
                        # cuento individualmente que en ese hogar id, 1 persona cumplió con ser universitario
                        personas_por_hogar[hogar_id] += 1 

        # Leer archivo de hogares
        with open(archivo_csv_hogares, 'r', encoding='utf-8') as archivo_hogares:
            hogares_reader = csv.reader(archivo_hogares, delimiter=';')
            next(hogares_reader)
            for row in hogares_reader:
                if int(row[year]) == anio and int(row[trim]) == trimestre:
                    codusu = row[CODUSU].strip()
                    nro_hogar = row[NRO_HOGAR].strip()
                    aglomerado = row[AGLOMERADO_HOGAR].strip()
                    pondera_hogar = int(row[PONDERA_HOG])
                    
                    diccionario_contador[aglomerado]['cant'] += pondera_hogar
                    
                    hogar_id = (codusu, nro_hogar)
                    if personas_por_hogar.get(hogar_id, 0) >= 2:
                        diccionario_contador[aglomerado]['cantesp'] += pondera_hogar

        # Obtener y mostrar el rankin de 5 aglomerados 
        resultados = sacar_porcentaje(diccionario_contador)
        print("Top 5 aglomerados con mayor porcentaje de hogares con mas de 2 personas"
        " con estudios universitarios o superiores finalizados:")
        for codigo, porcentaje in resultados[:5]:
            nombre = AGLOMERADOS.get(codigo, f"Aglomerado {codigo}")
            print(f"{nombre}: {porcentaje:.2f}%")
        if ok == True:
            return resultados
    except KeyError as e:
        print(f"Error: faltan columnas esperadas en los CSV. Columna faltante: {e}")
    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        print("Error: se esperaba un número pero se recibió otro dato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INCISO 5 SECCION B = Informar para cada aglomerado el porcentaje de viviendas ocupadas por sus propietarios.

def porcentaje_aglomerados_propietarios(archivocsv):
    """
    Imprime el porcentaje de viviendas ocupadas por propietarios en cada aglomerado.

    Parámetros:
    archivocsv (str): Ruta al archivo CSV con datos delimitados por punto y coma.

    Salida:
    Muestra en consola los porcentajes por aglomerado.

    Excepciones:
    KeyError: Si falta una columna esperada.
    FileNotFoundError: Si el archivo no existe.
    ValueError: Si hay un dato que no puede convertirse a número.
    Exception: Para cualquier otro error inesperado.
    """
    
    AGLOMERADOS = aglo_dict()
    
    #INDEX'S
    IDX_II7 = 37
    AGLOMERADO = 7
    PONDERA = 8
    
    # Inicializa el diccionario para contar las viviendas por aglomerado
    diccionariocontador = defaultcantidades()
    
    #AÑADO NUEVO VALOR EN EL DICCIONARIO PARA CONTAR LAS CANTIDADES DE VIVIENDAS OCUPADAS POR PROPIETARIOS
    for valor in diccionariocontador.values():
        valor['cantesp'] = 0
    try:
        with open(archivocsv, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo, delimiter=';')
            next(lector)
            
            for linea in lector:
                aglomerado_act = linea[AGLOMERADO].strip()
                II7_act = linea[IDX_II7].strip()
                pondera_act = int(linea[PONDERA])
                
                diccionariocontador[aglomerado_act]['cant'] += pondera_act
                if II7_act in ('1','2'):
                    diccionariocontador[aglomerado_act]['cantesp'] += pondera_act

        print("\nPorcentajes de viviendas ocupadas por sus propietarios:")
        listaporcentajes = sacar_porcentaje(diccionariocontador)
        for aglomerado, porcentaje in listaporcentajes:
            print(f"{AGLOMERADOS[aglomerado]}: {porcentaje:.2f}%")
    except KeyError as e:
        print(f"Error: faltan columnas esperadas en los CSV. Columna faltante: {e}")
    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        print("Error: se esperaba un número pero se recibió otro dato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INCISO 6 SECCION B = Informar el aglomerado con mayor cantidad de viviendas con más de dos ocupantes y sin baño.

def aglo_max_viviendas(diccionariocontador):
    """
    Retorna el código y la cantidad de viviendas del aglomerado con mayor cantidad total.

    Parámetros:
    diccionariocontador (dict): Diccionario con claves de aglomerado y valores con campo 'cant'.

    Retorno:
    tuple: (código de aglomerado, cantidad máxima de viviendas).
    """
    
    aglomerado_maximo = max(diccionariocontador.items(), key=lambda item: item[1]['cant'])
    return aglomerado_maximo[0], aglomerado_maximo[1]['cant']


def viviendas_esp(archivocsv):
    """
    Imprime el aglomerado con más viviendas que tienen más de dos ocupantes y no tienen baño.

    Parámetros:
    archivocsv (str): Ruta al archivo CSV con datos delimitados por punto y coma.

    Salida:
    Imprime en consola el nombre del aglomerado y la cantidad correspondiente.

    Excepciones:
    KeyError: Si falta una columna esperada.
    FileNotFoundError: Si el archivo no existe.
    ValueError: Si hay un dato que no puede convertirse a número.
    Exception: Para cualquier otro error inesperado.
    """
    
    AGLOMERADOS = aglo_dict()
    
    #INDEX'S 
    IX_TOT_OCUPANTES = 64
    AGLOMERADO = 7
    PONDERA = 8
    IV8_BAÑO = 19
    
    # Inicializa el diccionario para contar las viviendas por aglomerado
    diccionariocontador = defaultcantidades()
    try:
        with open(archivocsv, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo, delimiter=';')
            next(lector)  # Salta la primera línea (encabezados)
        
            for linea in lector:
                aglomerado_act = linea[AGLOMERADO].strip()
                pondera_act = int(linea[PONDERA])
                no_banio_act = linea[IV8_BAÑO].strip() == '2'
                total_ocupantes_act = int(linea[IX_TOT_OCUPANTES].strip())
            
                if (no_banio_act and (total_ocupantes_act > 2)):
                    diccionariocontador[aglomerado_act]['cant'] += pondera_act
        
        aglomax,cantmax = aglo_max_viviendas(diccionariocontador)  
        print(f"EL AGLOMERADO, {AGLOMERADOS[aglomax]}, TIENE LA MAYOR CANTIDAD DE VIVIENDAS CON MAS DE DOS OCUPANTES "
            f"Y SIN BAÑO CON UN TOTAL DE: {cantmax} VIVIENDAS")
    except KeyError as e:
        print(f"Error: faltan columnas esperadas en los CSV. Columna faltante: {e}")
    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        print("Error: se esperaba un número pero se recibió otro dato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#INCISO 7 SECCION B= Informar para cada aglomerado el porcentaje de personas que hayan cursado universitario o superior

def porc_aglo_estudios(archivocsv):
    """
    Calcula e imprime el porcentaje de personas con nivel universitario o superior por aglomerado.

    Parámetros:
    archivo_csv (str): Ruta al archivo CSV con datos delimitados por punto y coma.

    Salida:
    Muestra en consola los porcentajes por aglomerado.

    Excepciones:
    FileNotFoundError: Si el archivo no existe.
    Exception: Para otros errores inesperados durante el procesamiento.
    """
    
    AGLOMERADOS = aglo_dict()

    IND_ESTUDIO = 26 
    AGLOMERADO = 8
    PONDERA = 9
    
    # Inicializa el diccionario para contar las viviendas por aglomerado
    diccionariocontador = defaultcantidades()
    
    #CREO NUEVO VALOR EN EL DICCIONARIO PARA CONTAR LOS ESTUDIOS
    for valor in diccionariocontador.values():
        valor['cantesp'] = 0
    
    try:
        with open(archivocsv, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo, delimiter=';')
            next(lector)
        
                
            for linea in lector:
                try:
                    aglomerado_act = linea[AGLOMERADO].strip()
                    pondera_act = int(linea[PONDERA])
                    estudios_act = linea[IND_ESTUDIO].strip()
            
                    diccionariocontador[aglomerado_act]['cant'] += pondera_act
                
                    if  estudios_act in ('5','6'):
                        diccionariocontador[aglomerado_act]['cantesp'] += pondera_act
                except(IndexError,ValueError,KeyError) as e:
                    print(f'Error procesando la linea {linea}. {e}')

        print("\nPorcentajes de personas que han cursado al menos nivel universitario o superior:")
        listaporcentaje= sacar_porcentaje(diccionariocontador)
        
        for aglomerado, porcentaje in listaporcentaje:
            print(f"{AGLOMERADOS[aglomerado]}: {porcentaje:.2f}%")

    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INCISO 8 SECCION B = Informar las regiones en orden descendente según el porcentaje de inquilinos de cada una.

def crear_acumulador_inquilinos():
    """
    Crea y devuelve un diccionario para acumular el total de personas y la cantidad de inquilinos por región.

    Retorna:
    --------
    dict
        Diccionario con claves como códigos de región y valores como otro diccionario con las claves 'total' e 'inquilinos' inicializados en 0.
    """
    
    REGIONES = ['1', '40', '41', '42', '43', '44']
    return {i: {'total': 0, 'inquilinos': 0} for i in REGIONES}


def generar_porcentajes_inquilinos(estructura):
    """
    Calcula y devuelve una lista de tuplas con el porcentaje de inquilinos para cada región.

    Parámetros:
    -----------
    estructura : dict
        Diccionario con acumulados por región, debe contener claves 'total' e 'inquilinos' para cada región.

    Retorna:
    --------
    list of tuples
        Lista ordenada descendentemente de tuplas (región, porcentaje_inquilinos).
    """
    
    porcentajes = [] 
    for region, datos in estructura.items(): # recorro la estructura
        total= datos['total'] # a total le doy total de personas en esa region
        inquilinos= datos['inquilinos'] # a inquilinos le doy el total de inquilinos en esa region
        porcentaje = (inquilinos / total * 100 ) if total > 0 else 0.0 # saco porcentaje 
        porcentajes.append ((region, round (porcentaje, 2))) # agrego la region y el porcentaje a la lista
    porcentajes_ordenados = sorted(porcentajes, key=lambda x: x[1], reverse=True) # ordeno en forma descendiente
    return porcentajes_ordenados


def imprimir_region_inquilinos(archivo_csv):
    """
    Lee un archivo CSV y calcula el porcentaje de inquilinos por región, imprimiendo los resultados ordenados.

    Parámetros:
    -----------
    archivo_csv : str
        Ruta al archivo CSV que contiene los datos con columnas para región, cantidad ponderada y tipo de vivienda.

    Comportamiento:
    ---------------
    - Acumula el total y la cantidad de inquilinos por región.
    - Calcula los porcentajes de inquilinos para cada región.
    - Imprime una tabla con el porcentaje de inquilinos por región ordenada de mayor a menor.
    - Maneja excepciones relacionadas con archivos y datos faltantes o mal formateados.
    """
    
    nombres_regiones = {
        '1': 'Gran Buenos Aires',
        '40': 'Noroeste',
        '41': 'Noreste',
        '42': 'Cuyo',
        '43': 'Pampeana',
        '44': 'Patagonia'
    }
    try:
        with open (archivo_csv,encoding='utf-8') as archivo:
            reader = csv.reader(archivo,delimiter = ';')
            II7 = 37
            REGION = 5
            PONDERA = 8
            estructura = crear_acumulador_inquilinos()
            encabezado = next(reader)
            for row in reader:
                estructura[row[REGION]]['total'] += int (row[PONDERA])
                if row [II7] == '3':
                    estructura [row[REGION]]['inquilinos'] += int (row[PONDERA])
            porcentajes_ordenados= generar_porcentajes_inquilinos(estructura)
            print("\nPORCENTAJE DE INQUILINOS POR REGIÓN (Ordenado)")
            print("-----------------------------------------------")
            print("| Región               | Porcentaje         |")
            print("|----------------------|--------------------|")
            for r, p in porcentajes_ordenados:
                nombre_region = nombres_regiones.get(r)
                print(f'| {nombre_region:<20} | {p:>17}% |')

    except KeyError as e:
        print(f"Error: faltan columnas esperadas en los CSV. Columna faltante: {e}")
    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        print("Error: se esperaba un número pero se recibió otro dato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INCISO 9 SECCION B = Pedir al usuario que seleccione un aglomerado y a partir de la información contenida
# retornar una tabla que contenga la cantidad de personas mayores de edad según su nivel de estudios alcanzados.

def imprimir_tabla_formacion(estructuraPrincipal, nombre_aglomerado):
    """
    Imprime una tabla con la cantidad de personas mayores de edad
    distribuidas por nivel educativo, año y trimestre para un aglomerado dado.

    Parámetros:
    -----------
    estructuraPrincipal : dict
        Diccionario anidado con la estructura:
        { año: { trimestre: [prim_inc, prim_comp, sec_inc, sec_comp, sup] } }
    nombre_aglomerado : str
        Nombre descriptivo del aglomerado a mostrar.
    """
    
    print(f"\nNombre de Aglomerado: {nombre_aglomerado}\n")
    print(f"{'Año':^10} | {'Trimestre':^10} | {'Primario incompleto':^20} | {'Primario completo':^20} | "
        f"{'Secundario Incompleto':^20} | {'Secundario Completo':^20} | {'Superior o universitario':^20}")
    print("-" * 130) # hacemos el encabezado con las 3 lineas anteriores
    for anio in sorted(estructuraPrincipal.keys()): # ordenamos los anios
        for trimestre in sorted (estructuraPrincipal[anio].keys()): # ordenamos los trimestres
            prim_inc, prim_comp, sec_inc, sec_comp, sup = estructuraPrincipal[anio][trimestre] 
            print(f"{anio:^10} | {trimestre:^10} | {prim_inc:^20} | {prim_comp:^20} "
                f"| {sec_inc:^20} | {sec_comp:^20} | {sup:^20}")


def imprimir_formacion_por_aglomerado(archivo_csv):
    """
    Solicita al usuario seleccionar un aglomerado y muestra la distribución
    de niveles educativos de personas mayores de edad en dicho aglomerado.

    Parámetros:
    -----------
    archivo_csv : str
        Ruta al archivo CSV con datos individuales que incluye información educativa.
    """

    try:
        with open (archivo_csv,encoding='utf-8') as archivo:
            reader = csv.reader(archivo,delimiter = ';')
            encabezado = next(reader)
            aglomerados = aglo_dict()
            for codigo ,nombre in aglomerados.items():
                print (f"{codigo} {nombre}")
            numero_aglomerado= input (f"Ingrese el numero del aglomerado en el cual quiere obtener"
                "la informacion de nivel de estudios alcanzados de las personas que viven en el:")
            if not numero_aglomerado in aglomerados:
                print (f"Aglomerado inexistente")
            estructuraPrincipal = acumular_formacion_periodo(reader,numero_aglomerado)
            nombre_aglomerado = aglomerados[numero_aglomerado]
            imprimir_tabla_formacion(estructuraPrincipal,nombre_aglomerado)

    except KeyError as e:
        print(f"Error: faltan columnas esperadas en los CSV. Columna faltante: {e}")
    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        print("Error: se esperaba un número pero se recibió otro dato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


def procesar_fila_formacion(row,estructuraPrincipal,numero_aglomerado):
    """
    Procesa una fila del CSV y actualiza la estructura principal acumulando
    los conteos de personas mayores por nivel educativo, año y trimestre
    para un aglomerado específico.

    Parámetros:
    -----------
    row : list
        Lista con los datos de una fila del CSV.
    estructuraPrincipal : dict
        Diccionario donde se acumulan los datos por año y trimestre.
    numero_aglomerado : str
        Código del aglomerado para filtrar los datos relevantes.
    """
    
    PONDERA = 9
    COLUM_AGLOMERADO = 8
    EDAD = 13
    ANIO = 1
    TRIMESTRE = 2
    NIVEL_ED = 26
    try:
        if (int(row[EDAD]) > 18) and (numero_aglomerado == row[COLUM_AGLOMERADO]):
            if not (row [ANIO]) in estructuraPrincipal:
                estructuraPrincipal[row [ANIO]]= {} # si es un nuevo anio, creamos el diccionario de ese anio
            if not (row [TRIMESTRE]) in estructuraPrincipal[row [ANIO]]:
                estructuraPrincipal[row [ANIO]][row [TRIMESTRE]] = [0,0,0,0,0]  # EN DEFAULT cuando es nuevo trimestre
            if row [NIVEL_ED] == '1':
                estructuraPrincipal[row [ANIO]][row [TRIMESTRE]][0] += int (row [PONDERA])
            elif row [NIVEL_ED] == '2':
                estructuraPrincipal[row [ANIO]][row [TRIMESTRE]][1] += int (row [PONDERA])
            elif row [NIVEL_ED] == '3':
                estructuraPrincipal[row [ANIO]][row [TRIMESTRE]][2] += int (row [PONDERA])
            elif row [NIVEL_ED] == '4':
                estructuraPrincipal[row [ANIO]][row [TRIMESTRE]][3] += int (row [PONDERA])
            elif row [NIVEL_ED] == '5' or row [NIVEL_ED]== '6' :
                estructuraPrincipal[row [ANIO]][row [TRIMESTRE]][4] += int (row [PONDERA])
        # vamos cargando las personas que cumplen con cada condicion       
    except (IndexError,ValueError,KeyError) as e:
        print(f'Error procesando la fila {row}. {e}')


def acumular_formacion_periodo(reader,numero_aglomerado):
    """
    Lee todas las filas de un CSV (desde un reader) y acumula la información educativa
    para personas mayores por año y trimestre en un aglomerado determinado.

    Parámetros:
    -----------
    reader : iterable
        Objeto iterable (como csv.reader) que provee filas del archivo CSV.
    numero_aglomerado : str
        Código del aglomerado para filtrar los datos a acumular.

    Retorna:
    --------
    dict
        Diccionario acumulador con la estructura:
        { año: { trimestre: [prim_inc, prim_comp, sec_inc, sec_comp, sup] } }
    """
    
    try:
        # defino las variables para moverme en el archivo csv 
        estructuraPrincipal = {} ##creamos el diccionario principal
        for row in reader:
            procesar_fila_formacion(row,estructuraPrincipal,numero_aglomerado)
        return estructuraPrincipal  

    except KeyError as e:
        print(f"Error: faltan columnas esperadas en los CSV. Columna faltante: {e}")
    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        print("Error: se esperaba un número pero se recibió otro dato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")      

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INCISO 10 SECCION B = Pedir al usuario que seleccione dos aglomerados y a partir de la información
# contenida retornar una tabla que contenga el porcentaje de personas mayores de edad con secundario incompleto.

def imprimir_comparacion_aglomerados(estructuraAglomerado1,estructuraAglomerado2,
                nombre_aglomerado_1,nombre_aglomerado_2):
    """
    Imprime una tabla comparativa del porcentaje de personas mayores de edad
    con secundario incompleto entre dos aglomerados.

    Parámetros:
    -----------
    estructuraAglomerado1 : dict
        Diccionario con datos del primer aglomerado en formato:
        { año: { trimestre: [secIncTotal, totalPersonas] } }
    estructuraAglomerado2 : dict
        Diccionario con datos del segundo aglomerado (mismo formato que el primero).
    nombre_aglomerado_1 : str
        Nombre descriptivo del primer aglomerado.
    nombre_aglomerado_2 : str
        Nombre descriptivo del segundo aglomerado.
    """
    
    print("\nCOMPARACIÓN DE PORCENTAJE DE SECUNDARIO INCOMPLETO")
    print(f"{nombre_aglomerado_1} vs {nombre_aglomerado_2}\n")
    print(f"{'Año':<6}|{'Trimestre':<10}|{nombre_aglomerado_1[:15]:<15}|{nombre_aglomerado_2[:15]}")
    print("-" * 50)
    for anio in sorted(estructuraAglomerado1.keys()):
        for trimestre in sorted(estructuraAglomerado1[anio].keys()):
            secIncTotal1, total1 = estructuraAglomerado1[anio][trimestre]
            porcentaje1 = (secIncTotal1/total1) * 100 if total1 != 0 else 0
        # a partir de aca chequeo si el anio y el trimestre que se proceso del aglomerado 1, lo tiene el aglomerado 2
            if (anio in estructuraAglomerado2) and (trimestre in estructuraAglomerado2[anio]):
                secIncTotal2,total2 = estructuraAglomerado2 [anio][trimestre]
                porcentaje2 = (secIncTotal2 / total2) * 100 if total2 != 0 else 0
                print(f"{anio:<6} {trimestre:<10} {f'{porcentaje1:.1f}%':<15} {f'{porcentaje2:.1f}%'}")
                print("-" * 50)
    print("Nota: Porcentajes de personas > 18 años con secundario incompleto\n")

def procesar_aglo (numero_aglomerado,reader):
    """
    Procesa las filas de un CSV para acumular el total de personas mayores
    y la cantidad con secundario incompleto por año y trimestre para un aglomerado dado.

    Parámetros:
    -----------
    numero_aglomerado : str
        Código del aglomerado a filtrar.
    reader : iterable
        Objeto iterable que provee las filas del CSV (por ejemplo csv.reader).

    Retorna:
    --------
    dict
        Diccionario con estructura:
        { año: { trimestre: [secIncTotal, totalPersonas] } }
    """
    
    # defino la estructura que voy a utilizar y retornar
    estructuraAglomerado = {}
    # defino las variables para moverme en el archivo csv
    ANIO = 1
    TRIMESTRE = 2
    NIVEL_ED = 26
    PONDERA = 9
    COLUM_AGLOMERADO = 8
    EDAD = 13
    for row in reader:
        # consulto por la edad y por el aglomerado
        if ((row[EDAD]) > '18') and (row[COLUM_AGLOMERADO] == numero_aglomerado):
            if not row[ANIO] in estructuraAglomerado: # si ese anio no esta en la estructura, lo agregamos
                estructuraAglomerado[row [ANIO]] = {}
            # si dentro de ese anio no esta el trimestre, lo agregamos
            if not row[TRIMESTRE] in estructuraAglomerado[row [ANIO]]: 
                estructuraAglomerado [row [ANIO]][row [TRIMESTRE]] = [0,0] 
            if row[NIVEL_ED] == '3': 
                # primer valor= acumulador de secundario incompleto
                estructuraAglomerado [row [ANIO]][row [TRIMESTRE]][0] += int (row [PONDERA])
            # segundo valor= acumulador de personas mayores, que estan en el aglomerado 
            estructuraAglomerado[row[ANIO]][row[TRIMESTRE]][1] += int (row [PONDERA])
    return estructuraAglomerado

def comparacion_dos_aglomerados (archivo_csv):
    """
    Permite al usuario seleccionar dos aglomerados y compara el porcentaje
    de personas mayores con secundario incompleto entre ellos,
    mostrando una tabla comparativa.

    Parámetros:
    -----------
    archivo_csv : str
        Ruta del archivo CSV con datos educativos.
    """
    try:
        with open (archivo_csv,encoding='utf-8') as archivo:
            reader = csv.reader(archivo,delimiter = ';')
            next (reader)
            aglomerados = aglo_dict()
            for codigo,nombre in aglomerados.items():
                print (f'{codigo}  {nombre}')
            ## pido los aglomerados a comparar    
            numero_aglomerado_1= input (f'INGRESE EL NUMERO DEL ALGOMERADO 1:  ')
            numero_aglomerado_2 = input (f'INGRESE EL NUMERO DEL ALGOMERADO 2:  ')
            ## proceso aglomerado 1
            estructuraAglomerado1 = procesar_aglo (numero_aglomerado_1, reader)
            archivo.seek(1)
            estructuraAglomerado2 = procesar_aglo (numero_aglomerado_2, reader)
            ## me guardo el nombre de cada aglomerado para despues imprimirlos.
            nombre_aglomerado_1 = aglomerados[numero_aglomerado_1]
            nombre_aglomerado_2 = aglomerados[numero_aglomerado_2]
            imprimir_comparacion_aglomerados(
                estructuraAglomerado1,estructuraAglomerado2,nombre_aglomerado_1,nombre_aglomerado_2
            )

    except KeyError as e:
        print(f"Error: faltan columnas esperadas en los CSV. Columna faltante: {e}")
    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        print("Error: se esperaba un número pero se recibió otro dato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  EJERCICIO 11 - - - - - - - - - - - - - - - - - - - - - - -
# Pedir al usuario que seleccione un año, y busque en el último trimestre almacenado
# del mencionado año, el aglomerado con mayor porcentaje de viviendas de “Material
# precario” y el aglomerado con menor porcentaje de viviendas de “Material precario”.

def inicializar_algo_contadores ():
    """
    Inicializa un diccionario para contar personas en cada aglomerado,
    separando la cantidad de personas que viven en material precario
    y el total de personas.

    Retorna:
    --------
    dict
        Diccionario con claves siendo códigos de aglomerados y valores
        otro diccionario con las claves: 'nombre', 'personas_precario' y 'personas_totales'.
    """

    aglomerados = aglo_dict()
    estructura = {}
    for codigo, nombre in aglomerados.items():
        estructura[codigo] = {'nombre': nombre, 'personas_precario': 0, 'personas_totales': 0}
    return estructura


def imprimir_aglo_material_precario (aglo_mayor,aglo_menor,ultimo_trimestre,anio):
    """
    Imprime los resultados del aglomerado con mayor y menor porcentaje
    de personas viviendo en material precario para un año y trimestre dados.

    Parámetros:
    -----------
    aglo_mayor : tuple
        Tupla (codigo, datos) del aglomerado con mayor porcentaje, donde datos es un dict con 'nombre' y 'porcentaje'.
    aglo_menor : tuple
        Tupla (codigo, datos) del aglomerado con menor porcentaje, con igual estructura que aglo_mayor.
    ultimo_trimestre : int
        Número del último trimestre considerado en el análisis.
    anio : int
        Año analizado.
    """

    print(f"\n--- Resultados para el año {anio}, Trimestre {ultimo_trimestre} ---")
    print(f"Mayor % material precario: {aglo_mayor[1]['nombre']} ({aglo_mayor[1]['porcentaje']}%)")
    print(f"Menor % Material precario: {aglo_menor[1]['nombre']} ({aglo_menor[1]['porcentaje']}%)")


def procesar_material_precario (reader,anio):
    """
    Procesa un iterable CSV para calcular el porcentaje de personas
    viviendo en material precario en cada aglomerado, filtrando por año.

    Para cada trimestre dentro del año dado, se actualizan los contadores,
    manteniendo solo los datos del último trimestre.

    Parámetros:
    -----------
    reader : iterable
        Iterador sobre las filas del CSV (como csv.reader).
    anio : int
        Año a filtrar en los datos.

    Retorna:
    --------
    tuple
        (aglo_mayor, aglo_menor, ultimo_trimestre, anio), donde:
        - aglo_mayor y aglo_menor son tuplas (codigo, datos) 
            con el aglomerado con mayor y menor porcentaje respectivamente.
        - ultimo_trimestre es el número del último trimestre analizado.
        - anio es el año analizado.
    """

    col_anio = 1
    col_trimestre = 2
    col_material_techumbre = 89
    col_aglomerado = 7
    col_pondera = 8
    ultimo_trimestre = 0
    aglomerados = inicializar_algo_contadores()
    encabezado = next(reader)

    anio_encontrado = False 

    for row in reader:  
        if int(row[col_anio]) == anio:
            anio_encontrado = True
            trimestre_actual = int(row[col_trimestre])
            if ultimo_trimestre < trimestre_actual:
                ultimo_trimestre = trimestre_actual
                for aglo in aglomerados.values():
                    aglo['personas_precario'] = 0
                    aglo['personas_totales'] = 0
            if ultimo_trimestre == trimestre_actual:
                aglomerados[row[col_aglomerado]]['personas_totales'] += int(row[col_pondera])
                if row[col_material_techumbre] == 'Material Precario':
                    aglomerados[row[col_aglomerado]]['personas_precario'] += int(row[col_pondera])
    
    if not anio_encontrado:
        print(f"No se encuentra el año {anio} en el dataset.")
        return

    porcentaje_aglomerados = {}
    for codigo, datos in aglomerados.items():
        if datos['personas_totales'] > 0:
            porcentaje = (datos['personas_precario'] / datos['personas_totales']) * 100
            porcentaje_aglomerados[codigo] = {
                'nombre': datos['nombre'],
                'porcentaje': round(porcentaje, 2)}

    if porcentaje_aglomerados:
        items_ordenados = sorted(
            porcentaje_aglomerados.items(),
            key=lambda x: x[1]['porcentaje']
        )
        aglo_menor = items_ordenados[0]
        aglo_mayor = items_ordenados[-1]
        imprimir_aglo_material_precario(aglo_mayor, aglo_menor, ultimo_trimestre, anio)
    else:
        print(f"El año {anio} sí está, pero no hay datos suficientes para calcular porcentajes.")



def algomerado_material_precario (archivo_csv):
    """
    Solicita al usuario un año y muestra el aglomerado con mayor y menor
    porcentaje de personas viviendo en material precario para ese año.

    Parámetros:
    -----------
    archivo_csv : str
        Ruta al archivo CSV con los datos.

    Maneja errores comunes como archivo no encontrado, error en el formato
    de datos o entrada incorrecta del usuario.
    """

    try:
        with open (archivo_csv,encoding='utf-8') as archivo:
            reader = csv.reader(archivo,delimiter = ';')
            anio = int(input(
                "ENTRE EL 2016 Y EL 2024 INGRESE EL ANIO QUE QUIERE OBTENER "
                "EL AGLOMERADO CON MAYOR Y MENOR PORCENTAJE DE MATERIAL PRECARIO: "
            ))           
            if (anio < 2016) or (anio > 2024):
                print('AÑO INCORRECTO')
            else:
                procesar_material_precario(reader, anio)

    except KeyError as e:
        print(f"Error: faltan columnas esperadas en los CSV. Columna faltante: {e}")
    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        print("Error: se esperaba un número pero se recibió otro dato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - EJERCICIO 12 - - - - - - - - - - - - - - - - - - - - - - -
#​ A partir de la información del último trimestre almacenado en el sistema se debe
# retornar para cada aglomerado el porcentaje de jubilados que vivan en una vivienda
# con CONDICION_DE_HABITABILIDAD insuficiente.

def inicializar_estructura_jubilados():
    """
    Inicializa una estructura para almacenar datos de jubilados por aglomerado.

    Retorna:
    --------
    dict:
        Diccionario donde cada clave es el código de un aglomerado y el valor
        es otro diccionario con:
            - 'nombre': nombre del aglomerado,
            - 'jubilados_insuficiente': contador de jubilados en viviendas con habitabilidad insuficiente,
            - 'jubilados_totales': contador total de jubilados.
    """

    aglomerados = aglo_dict()
    estructura = {}

    for codigo,nombre in aglomerados.items():
        estructura[codigo] = {'nombre': nombre, 'jubilados_insuficiente': 0,'jubilados_totales': 0}
    return estructura


def jubilados_habitabilidad_insuficiente (archivo_csv_hogar,archivo_csv_individual):
    """
    Imprime el porcentaje de jubilados que viven en viviendas con habitabilidad insuficiente,
    agrupado por aglomerado, considerando solo datos del último trimestre del último año disponible.

    Parámetros:
    -----------
    archivo_csv_hogar : str
        Ruta al archivo CSV con datos de viviendas (delimitados por punto y coma).
    archivo_csv_individual : str
        Ruta al archivo CSV con datos individuales de personas (delimitados por punto y coma).

    Salida:
    -------
    Imprime en consola el porcentaje de jubilados en viviendas insuficientes por aglomerado.

    Excepciones:
    ------------
    KeyError: Si falta alguna columna esperada en los CSV.
    FileNotFoundError: Si alguno de los archivos no existe.
    ValueError: Si algún dato numérico no puede convertirse.
    Exception: Para cualquier otro error inesperado.
    """

    col_anio = 1
    col_codusu = 0
    col_trimestre = 2
    col_condi_habitabilidad = 91
    col_aglomerado = 8
    aglomerados = inicializar_estructura_jubilados()
    viviendas_insu = {}

    ult_anio, ult_trimestre = calcular_fechas(archivo_csv_hogar, 'mayor')
    try:     
        with open (archivo_csv_hogar, encoding='utf-8') as archivo:
            reader_hogar = csv.reader(archivo,delimiter = ';')
            next (reader_hogar) 

            for row in reader_hogar:
                # Solo procesamos filas del último trimestre
                if (int(row[col_anio]) == ult_anio and 
                    int(row[col_trimestre]) == ult_trimestre and 
                    row[col_condi_habitabilidad].strip() == 'Insuficiente'):
                    
                    viviendas_insu[row[col_codusu]] = row[col_aglomerado]

        with open (archivo_csv_individual, encoding='utf-8') as archivo:
            reader_individual = csv.reader(archivo,delimiter = ';')
            col_es_jubiliado = 29
            col_pondera = 9

            next (reader_individual)
            for row in reader_individual:
                if (
                        int(row[col_anio]) == ult_anio and
                        int(row[col_trimestre]) == ult_trimestre and
                        row[col_es_jubiliado].strip() == '1'
                    ):
                    aglomerados[(row[col_aglomerado])]['jubilados_totales'] += int(row[col_pondera])
                    if (row[col_codusu]) in viviendas_insu:
                        aglomerados[(row[col_aglomerado])]['jubilados_insuficiente'] += int(row[col_pondera])

        print("\n Porcentaje de jubilados en viviendas insuficientes por aglomerado, del ultimo trimestre :")
        print("{:<6} {:<40} {:<10}".format("Código", "Aglomerado", "Porcentaje"))
        print("-" * 45)

        for codigo, datos in aglomerados.items():
            porcentaje = (
                (datos['jubilados_insuficiente'] / datos['jubilados_totales']) * 100
                if datos['jubilados_totales'] > 0
                else 0
            )
            print("{:<6} {:<40} {:<10.2f}%".format(codigo, datos['nombre'],porcentaje))

    except KeyError as e:
        print(f"Error: faltan columnas esperadas en los CSV. Columna faltante: {e}")
    except FileNotFoundError:
        print("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        print("Error: se esperaba un número pero se recibió otro dato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - EJERCICIO 13 - - - - - - - - - - - - - - - - - - - - - - -

def cantidad_universitarios_en_vivienda_insuficiente_en_anio(individuos_csv, hogar_csv):
    """
    Imprime la cantidad de personas con estudios universitarios o superiores
    que viven en viviendas con condición de habitabilidad insuficiente,
    en el último trimestre del año ingresado por el usuario.

    Parámetros:
    archivocsv_individuos (str): Ruta al archivo CSV con datos individuales delimitados por punto y coma.
    archivocsv_hogar (str): Ruta al archivo CSV con datos de viviendas delimitados por punto y coma.

    Salida:
    Imprime en consola la cantidad de personas con nivel universitario o superior
    que viven en viviendas con habitabilidad insuficiente, para el último trimestre del año indicado.

    Excepciones:
    KeyError: Si falta una columna esperada en los CSV.
    FileNotFoundError: Si alguno de los archivos no existe.
    ValueError: Si hay un dato que no puede convertirse a número.
    PermissionError: Si no se poseen permisos para acceder a los archivos.
    TypeError: Si hay un error en el pasaje de parámetros.
    Exception: Para cualquier otro error inesperado.
    """

    ANIO = 1
    TRIM = 2
    NIVEL_ED_str = 178
    CODUSU = 0
    COND_HAB = 91
    PONDERA = 9

    try:
        anio_buscado = input('Ingrese el año a verificar: ').strip()
        
        viviendas_insu = {}  # codusu -> trimestre
        trimestres_disponibles = set()

        #Se busca el ultimo trimestre del año
        with open(hogar_csv, encoding='utf-8') as hogar:
            reader = csv.reader(hogar, delimiter=";")
            next(reader)
            for row in reader:
                if row[ANIO].strip() == anio_buscado:
                    trimestres_disponibles.add(row[TRIM].strip())

        if not trimestres_disponibles:
            print(f"No hay datos disponibles para el año {anio_buscado}.")
            return

        ultimo_trim = max(trimestres_disponibles, key=lambda x: int(x))

        # Se guardan la cantidad de viviendas insuficientes
        with open(hogar_csv, encoding='utf-8') as hogar:
            reader = csv.reader(hogar, delimiter=";")
            next(reader)
            for row in reader:
                if row[ANIO].strip() == anio_buscado and row[TRIM].strip() == ultimo_trim:
                    if row[COND_HAB].strip() == "Insuficiente":
                        codusu = row[CODUSU].strip()
                        viviendas_insu[codusu] = True

        cantidad = 0
        with open(individuos_csv, encoding='utf-8') as ind:
            reader = csv.reader(ind, delimiter=";")
            next(reader)
            for row in reader:
                if row[ANIO].strip() == anio_buscado and row[TRIM].strip() == ultimo_trim:
                    codusu = row[CODUSU].strip()
                    if codusu in viviendas_insu and row[NIVEL_ED_str].strip() == "Superior o universitario.":
                        cantidad += int(row[PONDERA])

        print(f'\nEn el último trimestre ({ultimo_trim}) del año {anio_buscado}, hubo {cantidad} personas')
        print('con estudios universitarios o superiores que vivían en viviendas con habitabilidad insuficiente.')

    except KeyError as e:
        print(f"Se accedió a una columna inexistente/erronea. Columna: {e}") #Solo puede pasar si está mal creado el dataset.
    except FileNotFoundError:
        print("No se encontró alguno de los archivos.")
    except ValueError:
        print("Se produjo un error al realizar la conversión.")
    except PermissionError:
        print("No se poseen permisos para acceder a los archivos.")
    except TypeError:
        print("Error en el pasaje de parametros.")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -