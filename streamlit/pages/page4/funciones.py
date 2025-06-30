import streamlit as st
import altair as alt
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.express as px
import sys
import time

current_dir = Path().resolve()
src_dir = current_dir.parents[2] / "src"

# Agrega src al sys.path (como string)
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

from funcionalidad import aglo_dict
from constantes import *

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX PAGE 4 - - - - - - - - - - - - - - - - - - - - - - - - - - 
def determinar_años(data):
    """
    Lee un archivo CSV y extrae la lista ordenada de años únicos presentes en la columna 'ANO4'.

    Parámetros:
    data (str): Ruta al archivo CSV.

    Retorna:
    list: Lista de años (enteros) ordenada ascendentemente.
    None: Si la columna 'ANO4' no existe en el archivo.
    Raises:
    Exception: Si ocurre un error al leer el archivo o procesar los datos.
    Warning: Si la columna 'ANO4' no existe, muestra un mensaje de advertencia en Streamlit.
    """
    try:
        with open(data, 'r') as file:
            df = pd.read_csv(file, sep=';')
        if 'ANO4' not in df.columns:
            st.warning("La columna de año no existe en el archivo.")
            return None
        else:
            # Extraer los años únicos, eliminar valores nulos y convertir a lista
            años = df['ANO4'].dropna().unique().tolist()
            # Ordenar la lista de años ascendentemente
            años.sort()
            return años
    except Exception as e:
        # Mostrar error en Streamlit si algo falla
        st.error(f"Error en determinar_años: {e}")
        # Retornar lista vacía para evitar errores posteriores
        return []
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 4.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 

def cantidades(option, data , años):
    """
    Calcula la cantidad total de viviendas (sin ponderar) y la cantidad para un año específico,
    basándose en hogares únicos identificados por CODUSU.

    Parámetros:
    option (int): Año seleccionado para filtrar.
    data (str): Ruta al archivo CSV.
    años (list): Lista de años para el cálculo del promedio.

    Retorna:
    tuple: (total_viviendas, viviendas_año), ambas como enteros.
    Raises:
    Exception: Si ocurre un error al leer el archivo o procesar los datos.
    Warning: Si faltan columnas requeridas en el DataFrame, muestra un mensaje de advertencia en Streamlit.
    """
    try:
        df = pd.read_csv(data, sep=';')
        
        if 'ANO4' not in df.columns or 'CODUSU' not in df.columns:
            st.warning("Faltan columnas requeridas ('ANO4' o 'CODUSU').")
            return 0, 0
        
        total_viviendas = int(df['CODUSU'].nunique())
        viviendas_año = int(df[df['ANO4'] == option]['CODUSU'].nunique())
        
        return total_viviendas, viviendas_año

    except Exception as e:
        st.error(f"Error en cantidades: {e}")
        return 0, 0

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 4.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 
def cant_viv_por_anio(option, anios):
    """
    Muestra en Streamlit la cantidad total de viviendas sin ponderar (por CODUSU),
    para un año seleccionado o para todos los años por separado.
    Parameters:
    - option: Año seleccionado (int) o "Todos" (str).
    - anios: Lista de años disponibles para el análisis.
    Raises:
    - Exception: Si ocurre un error al leer el archivo o procesar los datos.
    - Warning: Si faltan columnas requeridas en el DataFrame, muestra un mensaje de advertencia en Streamlit.
    - Warning: Si el calcuno no se puede realizar (cero viviendas), muestra un mensaje de advertencia en Streamlit.
    """
    try:
        # Cargo el archivo procesado de hogares
        df = pd.read_csv(PROCESSED_DATA_HOGAR, sep=';')

        # Verifico que existan las columnas necesarias 'ANO4' (año) y 'CODUSU' (identificador único de vivienda)
        if 'ANO4' not in df.columns or 'CODUSU' not in df.columns:
            st.warning("Faltan columnas requeridas ('ANO4' o 'CODUSU').")
            return

        # Si la opción es "Todos" años, hago el cálculo para cada año en la lista 'anios'
        if option == "Todos":
            data_lista = []
            for anio in anios:
                # Cuento viviendas únicas (CODUSU) filtrando por año
                viviendas_año = int(df[df['ANO4'] == anio]['CODUSU'].nunique())
                # Agrego el resultado para armar un DataFrame luego
                data_lista.append({'Año': anio, 'Viviendas': viviendas_año})

            # Creo un DataFrame con los resultados
            data = pd.DataFrame(data_lista)

            # Muestro la tabla en Streamlit
            st.dataframe(data)

            # Creo un gráfico de barras 
            chart = alt.Chart(data).mark_bar(size=40).encode(
                x=alt.X('Año:O', sort='ascending'),  # Eje X: año (categoría ordenada ascendente)
                y='Viviendas'                        # Eje Y: cantidad de viviendas
            ).properties(
                width=600,
                height=400,
                title='CANTIDAD DE VIVIENDAS POR AÑO (sin ponderar)'
            )

            # Muestro el gráfico en Streamlit, ajustado al ancho del contenedor
            st.altair_chart(chart, use_container_width=True)

        else:
            # Caso en que se selecciona un año específico

            # Llamo a la función 'cantidades' que devuelve total de viviendas y viviendas para el año
            total_viviendas, viviendas_año = cantidades(option, PROCESSED_DATA_HOGAR, anios)

            # Si no se pudo calcular (cero), muestro advertencia y salgo
            if total_viviendas == 0:
                st.warning("No se pudieron calcular las cantidades de viviendas.")
                return

            # Creo un DataFrame con el año seleccionado y la cantidad de viviendas para mostrar
            data = pd.DataFrame({
                'Año': [option],
                'Viviendas': [viviendas_año]
            })

            # Muestro la tabla en Streamlit
            st.dataframe(data)

            # Creo un gráfico de barras para el año seleccionado
            chart = alt.Chart(data).mark_bar(size=80).encode(
                x='Año',
                y=alt.Y('Viviendas', scale=alt.Scale(domain=[0, total_viviendas]))
            ).properties(
                width=300,
                height=400,
                title=f'CANTIDAD DE VIVIENDAS AÑO: {option} (sin ponderar)'
            )

            # Muestro el gráfico en Streamlit
            st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.error(f"Error al procesar los datos: {e}")
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.2 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 4.2 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 4.2 - - - - - - - - - - - - - - - - - - - - - - - - - -
def mostrar_grafico_torta_vivienda(option):
    """
    Muestra un gráfico de torta con la proporción de viviendas según su tipo.
    
    Parámetros:
    - option: Año seleccionado (int o 'Todos').
    Raises:
    - FileNotFoundError: Si no se encuentra el archivo de datos.
    - Exception: Si ocurre un error inesperado durante el procesamiento.
    - Warning: Si faltan columnas necesarias en el DataFrame.
    """

    try:
        df_hogar = pd.read_csv(PROCESSED_DATA_HOGAR, delimiter=';')

        if 'ANO4' not in df_hogar.columns or 'IV1' not in df_hogar.columns:
            st.warning("Faltan columnas necesarias para el análisis ('ANO4' o 'IV1').")
            return

        # Filtrar si se eligió un año específico
        if option != "Todos":
            df_hogar = df_hogar[df_hogar["ANO4"] == option]

        # Mapear códigos de tipo de vivienda
        mapa_vivienda = {
            1: "Casa",
            2: "Departamento",
            3: "Pieza de inquilinato",
            4: "Hotel/pensión",
            5: "Local no construido",
            6: "Otro"
        }
        df_hogar["tipo_vivienda"] = df_hogar["IV1"].map(mapa_vivienda)

        # Agrupar y contar
        conteo = df_hogar["tipo_vivienda"].value_counts().reset_index()
        conteo.columns = ["Tipo de vivienda", "Cantidad"]

        # Gráfico de torta 
        figura = px.pie(
            conteo,
            names="Tipo de vivienda",
            values="Cantidad",
            title=f"Proporción de viviendas según tipo - {option}"
        )
        figura.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(figura, use_container_width=True)
    
    except FileNotFoundError:
        st.error("No se encontró el archivo de datos.")
    except Exception as e:
        st.error(f"Error al generar el gráfico de torta: {e}")

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.3 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 4.3 - - - - - - - - - - - - - - - - - - - - - - - - - - 

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 4.3 - - - - - - - - - - - - - - - - - - - - - - - - - -
def material_predominante_por_aglomerado(option, anios): 
    """
    Determina el material de piso predominante por aglomerado, filtrado por año (y trimestre si aplica).
    Si se elige 'Todos', analiza cada año por separado y muestra el total acumulado.

    Parameters:
    - option: Año seleccionado o "Todos"
    - anios: Lista de años disponibles
    raises:
    - FileNotFoundError: Si no se encuentra el archivo de datos.
    - Exception: Si ocurre un error inesperado durante el procesamiento.
    - Warning: Si faltan columnas necesarias en el DataFrame.
    """
    materiales_piso = {
        '1': 'Mosaico, baldosa, madera, cerámica, alfombra',
        '2': 'Cemento, ladrillo fijo',
        '3': 'Ladrillo suelto, tierra',
    }
    try:
        datos_hogar = pd.read_csv(PROCESSED_DATA_HOGAR, delimiter=';')

        columnas = {'ANO4', 'TRIMESTRE', 'AGLOMERADO', 'IV3', 'CODUSU'}
        if not columnas.issubset(datos_hogar.columns):
            st.warning("Faltan columnas necesarias para el análisis.")
            return

        datos_hogar['ANO4'] = pd.to_numeric(datos_hogar['ANO4'], errors='coerce')
        datos_hogar['TRIMESTRE'] = pd.to_numeric(datos_hogar['TRIMESTRE'], errors='coerce')
        datos_hogar['AGLOMERADO'] = datos_hogar['AGLOMERADO'].astype(str)
        datos_hogar['IV3'] = datos_hogar['IV3'].astype(str).str.strip()
        datos_hogar['CODUSU'] = datos_hogar['CODUSU'].astype(str)

        datos_hogar['MATERIAL_PISO'] = datos_hogar['IV3'].map(materiales_piso, na_action='ignore')
        datos_hogar = datos_hogar.dropna(subset=['MATERIAL_PISO','AGLOMERADO'])
        datos_hogar = datos_hogar.drop_duplicates(subset='CODUSU')

        if option != "Todos":
            selec_anio = int(option)
            trimestres = sorted(datos_hogar[datos_hogar['ANO4'] == selec_anio]['TRIMESTRE'].dropna().unique(), reverse=True)
            selec_trim = st.selectbox('Seleccione un trimestre', trimestres)
            filtrado = datos_hogar[(datos_hogar['ANO4'] == selec_anio) & (datos_hogar['TRIMESTRE'] == selec_trim)]
            
            if filtrado.empty:
                st.warning(f'No hay datos para el año {selec_anio} y trimestre {selec_trim}.')
                return
            conteo = filtrado.groupby(['AGLOMERADO', 'MATERIAL_PISO']).size().reset_index(name='cantidad')
            titulo = f'Material predominante - Año {selec_anio}, Trimestre {selec_trim}'

        # Si se seleccionó "Todos"
        else:
            lista_conteo = []
            for anio in anios:
                datos_anio = datos_hogar[datos_hogar['ANO4'] == anio]
                conteo_anio = datos_anio.groupby(['AGLOMERADO', 'MATERIAL_PISO']).size().reset_index(name='cantidad')
                lista_conteo.append(conteo_anio)
            conteo = pd.concat(lista_conteo).groupby(['AGLOMERADO', 'MATERIAL_PISO'])['cantidad'].sum().reset_index()
            titulo = 'Material predominante - Todos los años'

        # Agrupar
        conteo['AGLOMERADO'] = conteo['AGLOMERADO'].map(lambda x: aglo_dict().get(x, f'Aglomerado {x}'))
        tabla = conteo.pivot(index='AGLOMERADO', columns='MATERIAL_PISO', values='cantidad').fillna(0)

        st.subheader(titulo)
        st.dataframe(tabla)

        fig, ax = plt.subplots(figsize=(12, 8))
        tabla.plot.barh(ax=ax)
        ax.set_title("Distribución de materiales de piso por aglomerado")
        ax.set_xlabel("Cantidad de viviendas")
        plt.tight_layout()
        st.pyplot(fig)
        
    except FileNotFoundError:
        st.error("No se encontró el archivo especificado.")
    except Exception as e:
        st.error(f"Error: {e}")
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.4 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 4.4 - - - - - - - - - - - - - - - - - - - - - - - - - - 
def mostrar_aglo (aglomerado):
    """
    Muestra el nombre del aglomerado seleccionado.
    Parameters:
        aglomerado (int): Valor del aglomerado seleccionado.
    Returns:
        Mapeo a string con el nombre del aglomerado.
    """
    return f' {aglo_dict()[aglomerado]}'

def mostrar_grafico_prop_banio(estructura):
    df = pd.DataFrame([
        {'Aglomerado': aglo, 'Proporción con baño dentro del hogar (%)': valor}
        for aglo, valor in estructura.items()
    ])

    ordenada = df.sort_values("Proporción con baño dentro del hogar (%)", ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(ordenada['Aglomerado'], ordenada['Proporción con baño dentro del hogar (%)'])
    ax.set_xlabel('Proporción con baño dentro del hogar (%)')
    ax.set_ylabel('Aglomerado')
    ax.set_title('Proporción de viviendas con baño dentro del hogar')
    ax.grid()

    return fig

def evaluarTodos(hogares, anios, aglomerados):
    """
    Calcula la proporción de viviendas con baño dentro del hogar por aglomerado,
    considerando todos los años disponibles.

    Parameters:
        hogares: DataFrame con datos de hogares.
        anios: Lista de años disponibles para el análisis.
        aglomerados: Lista de aglomerados a evaluar.

    Returns:
        dic_x_aglo: Diccionario con la proporción de viviendas con baño dentro del hogar por aglomerado.
    """
    dic_x_aglo = {}
    for aglo in aglomerados:
        casas_totales = 0
        cant_con_banio = 0
        clave = f'{mostrar_aglo(aglo)}'
        for anio in anios:
            filtro = (hogares['AGLOMERADO'] == aglo) & (hogares['ANO4'] == anio)
            casas_totales += (hogares[filtro]['PONDERA'].sum())
            cant_con_banio += (hogares[filtro & (hogares['IV9']== 1)]['PONDERA'].sum())
        proporcion = cant_con_banio/casas_totales if casas_totales != 0 else 0
        dic_x_aglo[clave] = round(proporcion*100,2)
    return dic_x_aglo

def evaluarUnAño(hogares, opcion, aglomerados):
    dic_un_anio={}
    for aglo in aglomerados:
        clave = f'{mostrar_aglo(aglo)}'
        casas_totales = (hogares[(hogares['ANO4'] == opcion) & (hogares['AGLOMERADO']== aglo)]['PONDERA'].sum())
        cant_con_banio = hogares[(hogares['ANO4'] == opcion) & (hogares['AGLOMERADO']==aglo) & (hogares['IV9'] == 1)]['PONDERA'].sum()
        proporcion = cant_con_banio/casas_totales if casas_totales != 0 else 0
        dic_un_anio[clave] = ((proporcion*100).round(2))
    return dic_un_anio
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 4.2 - - - - - - - - - - - - - - - - - - - - - - - - - -


def banio_dentro_hogar_aglomerado(opcion, anios):
    """
    Muestra la proporción de viviendas con baño dentro del hogar por aglomerado,
    filtrado por año y trimestre si es necesario.
    
    Parameters
    ----------
    opcion : str o int
        Año seleccionado o "Todos"
    anios : list
        Lista de años disponibles para el análisis
    Raises:
    -------
    FileNotFoundError: Si no se encuentra el archivo de datos.
    ValueError: Si se espera un número pero se recibe otro dato.
    Warning: Si faltan columnas requeridas en el DataFrame, muestra un mensaje de advertencia en Streamlit.
    """
    try:
        hogares = pd.read_csv(PROCESSED_DATA_HOGAR, delimiter=';', encoding='utf-8')
        columnas_necesarias = {'ANO4', 'IV9', 'AGLOMERADO', 'PONDERA'}
        if not columnas_necesarias.issubset(hogares.columns):
            st.warning("Faltan columnas requeridas ('PONDERA' , 'ANO4' o 'IV9').")
            
        
        hogares['ANO4'] = pd.to_numeric(hogares['ANO4'], errors='coerce')
        hogares['IV9'] = pd.to_numeric(hogares['IV9'], errors='coerce')
        hogares['PONDERA'] = pd.to_numeric(hogares['PONDERA'], errors='coerce')
        hogares['AGLOMERADO'] = hogares['AGLOMERADO'].astype(str)

        aglomerados = (hogares['AGLOMERADO'].unique())

        if opcion == 'Todos':
            estructura = evaluarTodos(hogares, anios, aglomerados)     
        else:
            estructura = evaluarUnAño(hogares, opcion, aglomerados)
        fig =  mostrar_grafico_prop_banio(estructura)
        st.pyplot(fig)
        #aglo_con_banio = hogares.groupby([ANO4, AGLOMERADO]).apply (calcular_prop).reset_index()  
    except FileNotFoundError:
        st.error("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        st.error("Error: se esperaba un número pero se recibió otro dato.")

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.5 - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Inciso pag 4
def evolucion_tenencia(option):
    """
    Versión optimizada que recibe:
    - option: int (año específico) o 'Todos' (string)
    - anios: parámetro opcional (se mantiene por compatibilidad)
    Raises:
    Exception: Si ocurre un error al leer el archivo o procesar los datos.
    """
    ##chequeo si ingreso todos o un anio
    analizar_todos_los_años = option == 'Todos'
    año_especifico = int(option) if not analizar_todos_los_años else None

    # 2. Diccionario de regímenes
    regimen_tenencia = {
        '1': 'Propietario de la vivienda y el terreno',
        '2': 'Propietario de la vivienda',
        '3': 'Inquilino',
        '4': 'Ocupante por pago de impuestos/expensas',
        '5': 'Ocupante en relación de dependencia',
        '6': 'Ocupante gratuito (con permiso)',
        '7': 'Ocupante de hecho (sin permiso)',
        '8': 'Está en sucesión',
    }

    # 3. Carga y limpieza de datos
    try:
        df = pd.read_csv(PROCESSED_DATA_HOGAR, sep=';')
        df = df.dropna(subset=['CODUSU', 'ANO4', 'II7', 'AGLOMERADO']).copy()
        df['II7'] = df['II7'].astype(str)  # Asegurar tipo string para II7
        df = df.drop_duplicates(subset=['CODUSU', 'ANO4'])  # Viviendas únicas
    except Exception as e:
        st.error(f"Error crítico: {str(e)}")

    # 4. Interfaz de usuario 
    st.title("Análisis de Régimen de Tenencia")
    
    # Selección de aglomerado
    aglomerados = aglo_dict()
    aglo_nombre = st.selectbox(
        "Seleccione un aglomerado:",
        options=list(aglomerados.values()),
        key="aglomerado_tenencia"
    )
    aglo_codigo = next(k for k, v in aglomerados.items() if v == aglo_nombre)

    # Selección de regímenes
    st.subheader("Selección de Tipos de Tenencia")
    todos_los_regimenes = st.checkbox("Seleccionar todos", value=True, key="check_todos_regimenes")
    
    opciones_ordenadas = sorted(regimen_tenencia.items(), key=lambda x: x[1])  # Ordenar por descripción
    regimenes_seleccionados = (
        [k for k, _ in opciones_ordenadas] 
        if todos_los_regimenes 
        else st.multiselect(
            "Regímenes a visualizar:",
            options=[k for k, _ in opciones_ordenadas],
            format_func=lambda x: regimen_tenencia[x],
            key="multiselect_regimenes"
        )
    )

    #  Generación de resultados (boton)
    if st.button("Generar análisis", type="primary", key="btn_analisis"):
        if not regimenes_seleccionados:
            st.warning("Seleccione al menos un régimen")

        # Filtrar por aglomerado y regímenes
        df_filtrado = df[
            (df['AGLOMERADO'] == int(aglo_codigo)) & 
            (df['II7'].isin(regimenes_seleccionados))
        ]

        if analizar_todos_los_años:
            # Mostrar tipos de tenencia
            st.write("**Analizando:** " + ", ".join([regimen_tenencia[r] for r in regimenes_seleccionados]))
            
            # Calcular y mostrar datos
            evolucion = (
                df_filtrado.groupby(['ANO4', 'II7'])
                .size()
                .unstack()
                .fillna(0)
                .apply(lambda x: x/x.sum()*100, axis=1)
                .rename(columns=regimen_tenencia)
                .round(1)
            )
            
            # Gráfico mínimo
            fig, ax = plt.subplots()
            evolucion.plot(kind='line', ax=ax)
            st.pyplot(fig)
            
            # Tabla compacta
            st.write(evolucion)

        else:
            # Análisis para año específico
            df_año = df_filtrado[df_filtrado['ANO4'] == año_especifico]
            if df_año.empty:
                st.warning(f"No hay datos para {año_especifico}")

            distribucion = (
                df_año['II7']
                .value_counts(normalize=True)
                .mul(100)
                .rename(index=regimen_tenencia)
                .sort_values()
            )
            
            fig, ax = plt.subplots(figsize=(10, 6))
            distribucion.plot(kind='barh', color='#3498db', ax=ax)
            ax.set_title(f"Distribución en {aglo_nombre} ({año_especifico})")
            ax.set_xlabel('Porcentaje (%)')
            st.pyplot(fig)
            st.dataframe(distribucion.round(1).to_frame('Porcentaje (%)'))
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.6 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 4.6 - - - - - - - - - - - - - - - - - - - - - - - - - - 

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 4.6 - - - - - - - - - - - - - - - - - - - - - - - - - -
def viviendas_en_villa_por_aglomerado(option, anios):
    """
    Informa la cantidad y porcentaje de viviendas ubicadas en villas de emergencia por aglomerado,
    filtrado por año y trimestre.

    Parameters
    ----------
    option : str o int
        Año seleccionado o "Todos"
    anios : list
        Lista de años disponibles

    Returns
    -------
    None
    
    Raises:
    -------
    FileNotFoundError: Si no se encuentra el archivo de datos.
    Exception: Si ocurre un error inesperado durante el procesamiento.
    Warning: Si faltan columnas necesarias en el DataFrame.
    """
    try:
        datos_hogar = pd.read_csv(PROCESSED_DATA_HOGAR, delimiter=';')

        columnas = {'ANO4', 'TRIMESTRE', 'AGLOMERADO', 'IV12_3', 'CODUSU'}
        if not columnas.issubset(datos_hogar.columns):
            st.warning("Faltan columnas necesarias para el análisis.")
            return

        datos_hogar['ANO4'] = pd.to_numeric(datos_hogar['ANO4'], errors='coerce')
        datos_hogar['TRIMESTRE'] = pd.to_numeric(datos_hogar['TRIMESTRE'], errors='coerce')
        datos_hogar['IV12_3'] = pd.to_numeric(datos_hogar['IV12_3'], errors='coerce')
        datos_hogar['AGLOMERADO'] = datos_hogar['AGLOMERADO'].astype(str)
        datos_hogar['CODUSU'] = datos_hogar['CODUSU'].astype(str)

        datos_hogar = datos_hogar[datos_hogar['IV12_3'].isin([1, 2])]
        datos_hogar = datos_hogar.drop_duplicates(subset='CODUSU')

        if option != "Todos":
            selec_anio = int(option)
            trimestres = sorted(datos_hogar[datos_hogar['ANO4'] == selec_anio]['TRIMESTRE'].dropna().unique(), reverse=True)
            selec_trim = st.selectbox("Seleccionar trimestre", trimestres)
            filtrado = datos_hogar[(datos_hogar['ANO4'] == selec_anio) & (datos_hogar['TRIMESTRE'] == selec_trim)]

            if filtrado.empty:
                st.warning("No hay datos disponibles para ese año y trimestre.")
                return
            titulo = f"Viviendas en villa - Año {selec_anio}, Trimestre {selec_trim}"

        else:
            lista_filtrados = []
            for anio in anios:
                datos_anio = datos_hogar[datos_hogar['ANO4'] == anio]
                lista_filtrados.append(datos_anio)
            filtrado = pd.concat(lista_filtrados)
            titulo = "Viviendas en villa - Todos los años"

        total_viv = filtrado.groupby('AGLOMERADO').size().rename('total')

        en_villa = filtrado[filtrado['IV12_3'] == 1]
        cantidad_villa = en_villa.groupby('AGLOMERADO').size().rename('VIVIENDAS_EN_VILLA')

        resumen = pd.concat([cantidad_villa, total_viv], axis=1).fillna(0)
        resumen['VIVIENDAS_EN_VILLA'] = resumen['VIVIENDAS_EN_VILLA'].astype(int)
        resumen['PORCENTAJE'] = (resumen['VIVIENDAS_EN_VILLA'] / resumen['total']) * 100
        resumen = resumen.reset_index()

        resumen['AGLOMERADO'] = resumen['AGLOMERADO'].map(lambda x: aglo_dict().get(x, f"Aglomerado {x}"))
        resumen = resumen.sort_values(by='VIVIENDAS_EN_VILLA', ascending=False)

        st.subheader(titulo)
        st.dataframe(resumen[['AGLOMERADO', 'VIVIENDAS_EN_VILLA', 'PORCENTAJE']].round(2))

    except FileNotFoundError:
        st.error("No se encontró el archivo especificado.")
    except Exception as e:
        st.error(f"Error inesperado: {e}")

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.7 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 4.7 - - - - - - - - - - - - - - - - - - - - - - - - - - 
def calcular_porcentaje_habitabilidad(archivo_csv_hogares, anio_filtro=None):
    """
    Calcula el porcentaje de viviendas por condición de habitabilidad en cada aglomerado.

    Parámetros:
    archivo_csv_hogares (str): Ruta al archivo CSV de hogares.
    anio_filtro (int, opcional): Año específico a filtrar (columna 'ANO4'). Si None, se usan todos los años.

    Retorna:
    pd.DataFrame: Tabla con columnas ['AGLOMERADO', 'CONDICION_DE_HABITABILIDAD', 'AÑO', 'Porcentaje (%)'].
    None: Si faltan columnas necesarias.
    
    Raises:
    st.error: Faltan columnas necesarias en el CSV.
    """
    
    df = pd.read_csv(archivo_csv_hogares, delimiter=';')

    columnas_necesarias = {'AGLOMERADO', 'CONDICION_DE_HABITABILIDAD', 'ANO4'}
    if not columnas_necesarias.issubset(df.columns):
        st.error("Faltan columnas necesarias en el CSV.")
        return None
    
    if anio_filtro is not None:
        # Filtra el dataframe por el año indicado
        df = df[df['ANO4'] == anio_filtro]

    # Cuenta la cantidad de registros por cada combinación de aglomerado + condición de habitabilidad
    grupo = df.groupby(['AGLOMERADO', 'CONDICION_DE_HABITABILIDAD']).size().reset_index(name='Cantidad')

    # Suma total de viviendas por aglomerado (para calcular el %)
    total_x_aglomerado = grupo.groupby('AGLOMERADO')['Cantidad'].sum().reset_index(name='TOTAL_AGLOMERADO')

    # Combina las dos tablas para poder calcular el porcentaje
    grupo = grupo.merge(total_x_aglomerado, on='AGLOMERADO')

    # Calcula el porcentaje de cada condición dentro del aglomerado
    grupo['Porcentaje (%)'] = (grupo['Cantidad'] / grupo['TOTAL_AGLOMERADO']) * 100
    grupo['Porcentaje (%)'] = grupo['Porcentaje (%)'].round(2)

    # Agrega columna del año (para que se vea en la exportación)
    grupo['AÑO'] = anio_filtro if anio_filtro is not None else 'Todos'

    return grupo[['AGLOMERADO', 'CONDICION_DE_HABITABILIDAD', 'AÑO', 'Porcentaje (%)']]


#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 4.7 - - - - - - - - - - - - - - - - - - - - - - - - - -


def exportar_porcentaje_habitabilidad(option, anios):
    """
    Exporta a CSV el porcentaje de viviendas por condición de habitabilidad para un año seleccionado,
    o para todos los años.

    Parámetros:
    option (str o int): 'Todos' o un año específico.
    anios (list): Lista de años disponibles para filtrar.
    """

    st.title("Porcentaje de viviendas por Condición de Habitabilidad")
    st.write("Este reporte muestra el porcentaje de viviendas por condición de habitabilidad en cada aglomerado.")
    st.write(f"**Año seleccionado:** {option}")
    st.write("¿Desea continuar?")
    
    hacer = st.button("Continuar")
    
    if hacer:
        # Decide si filtrar por año o no
        if option == 'Todos':
            df_resultado = calcular_porcentaje_habitabilidad(PROCESSED_DATA_HOGAR)
            nombre = "porcentaje_habitabilidad_todos.csv"
        else:
            df_resultado = calcular_porcentaje_habitabilidad(PROCESSED_DATA_HOGAR, anio_filtro=int(option))
            nombre = f"porcentaje_habitabilidad_{option}.csv"

        if df_resultado is not None:
            # Barra de progreso visual
            barra_placeholder = st.empty()
            with barra_placeholder:
                barra = st.progress(0)
                for pct in range(0, 101):
                    time.sleep(0.02)
                    barra.progress(pct)
            barra_placeholder.empty()

            # Muestra tabla en pantalla
            st.success("¡Reporte generado con éxito!")
            st.dataframe(df_resultado)

            # Prepara CSV en memoria para descarga
            csv_data = df_resultado.to_csv(index=False, sep=';').encode('utf-8')

            # Botón para descargar CSV
            st.download_button(
                label="📥 Descargar CSV",
                data=csv_data,
                file_name=nombre,
                mime='text/csv'
            )
