import streamlit as st
import json
import folium
from streamlit_folium import folium_static
import pandas as pd
import altair as alt
from pathlib import Path
import sys
import matplotlib.pyplot as plt
import plotly.express as px


current_dir = Path().resolve()
src_dir = current_dir.parents[2] / "src"

# Agrega src al sys.path (como string)
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

from funcionalidad import aglo_dict
from constantes import *

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 5.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 5.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 5.1 - - - - - - - - - - - - - - - - - - - - - - - - - -
def mostrar_desocupacion_por_estudios():
    """
    Muestra un gráfico de barras horizontales con la cantidad de personas desocupadas
    según el nivel educativo alcanzado, para un año y trimestre seleccionados.
    
    Raises:
    FileNotFoundError: Si no se encuentra el archivo de datos procesados.
    KeyError: Error al procesar los datos de las columnas.
    Warning: Si no hay datos de personas desocupadas para el período seleccionado.
    """

    try:
        df = pd.read_csv(PROCESSED_DATA_INDIVIDUAL, sep=";")

        # Filtros por año y trimestre
        anios = sorted(df["ANO4"].dropna().unique())
        anio = st.selectbox("Seleccioná un año", anios)
        trimestres = sorted(df[df["ANO4"] == anio]["TRIMESTRE"].dropna().unique())
        trimestre = st.selectbox("Seleccioná un trimestre", trimestres)

        # Tomo los datos filtrados por año, trimestre y estado de desocupación
        df_filtrado = df[(df["ANO4"] == anio) & (df["TRIMESTRE"] == trimestre)]
        df_desocupados = df_filtrado[df_filtrado["ESTADO"] == 2]

        conteo = df_desocupados.groupby("NIVEL_ED_str")["PONDERA"].sum()
        conteo = conteo.sort_values()
        conteo = conteo.reset_index()
        conteo.columns = ["Nivel educativo", "Cantidad"]
        if conteo.empty:
            st.warning("No hay datos de personas desocupadas para el período seleccionado.")

        # Gráfico de barras horizontales
        figura = px.bar(
            conteo,
            x="Cantidad",
            y="Nivel educativo",
            orientation="h",
            title= (f"Personas desocupadas según estudios alcanzados - {anio} T{trimestre}"),
            labels={"Cantidad": "Cantidad de desocupados", "Nivel educativo": "Nivel educativo alcanzado"}
        )
        st.plotly_chart(figura)

    except FileNotFoundError:
        st.error("No se encontró el archivo de datos procesados.")
    except KeyError:
        st.error("Error al procesar los datos. Verifique las columnas requeridas.")
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 5.2 - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 5.2 - - - - - - - - - - - - - - - - - - - - - - - - - - 
def calcular_tasa(datos_empleo, tipo='desempleo'):
    """
    Calcula la tasa de desempleo ponderada para un conjunto de registros.

    Parameters
    ----------
    datos_empleo : pd.DataFrame
        Subconjunto de registros con las columnas 'PONDERA' y 'CONDICION_LABORAL'.

    Returns
    -------
    float
        Tasa de desempleo expresada en porcentaje.
    """
    
    ocupados = datos_empleo[datos_empleo['CONDICION_LABORAL'].str.startswith('Ocupado')]['PONDERA'].sum()
    desocupados = datos_empleo[datos_empleo['CONDICION_LABORAL'] == 'Desocupado.']['PONDERA'].sum()
    total = ocupados + desocupados
    if tipo == 'empleo':
        return (ocupados / total) * 100 if total != 0 else 0
    elif tipo== 'desempleo':
        return (desocupados / total) * 100 if total != 0 else 0


#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 5.2 - - - - - - - - - - - - - - - - - - - - - - - - - -
def evolucion_desempleo():
    """
    Grafica la evolución de la tasa de desempleo a lo largo del tiempo,
    ya sea a nivel país o filtrado por un aglomerado en particular.

    Returns
    -------
    None
        Muestra un gráfico con la evolución de la tasa de desempleo.
    Raises
    ------
        FileNotFoundError
            Si no se encuentra el archivo de datos procesados.
        TypeError
            Si hay un error en los parámetros de llamada de la función.
        Warning
            Si faltan columnas necesarias para calcular la tasa de desempleo.
    """
    try:
        datos_personas = pd.read_csv(PROCESSED_DATA_INDIVIDUAL, delimiter=';')

        columnas = {'ANO4', 'TRIMESTRE', 'PONDERA', 'CONDICION_LABORAL', 'AGLOMERADO'}
        if not columnas.issubset(datos_personas.columns):
            st.warning("Faltan columnas necesarias para calcular desempleo.")
            return

        datos_personas['ANO4'] = pd.to_numeric(datos_personas['ANO4'], errors='coerce')
        datos_personas['TRIMESTRE'] = pd.to_numeric(datos_personas['TRIMESTRE'], errors='coerce')
        datos_personas['PONDERA'] = pd.to_numeric(datos_personas['PONDERA'], errors='coerce')
        datos_personas['AGLOMERADO'] = datos_personas['AGLOMERADO'].astype(str)
        datos_personas['CONDICION_LABORAL'] = datos_personas['CONDICION_LABORAL'].astype(str)
        
        aglomerados = sorted(datos_personas['AGLOMERADO'].unique())
        selec_aglo = st.selectbox('Seleccione un aglomerado (Opcional)', ['Total País'] + aglomerados)
        
        if selec_aglo != 'Total País':
            datos_personas = datos_personas[datos_personas['AGLOMERADO'] == selec_aglo]
            nombre_aglomerado = aglo_dict().get(selec_aglo,selec_aglo)
        else:
            nombre_aglomerado = 'Total País'
        
        datos_personas = datos_personas.dropna(subset=['ANO4','TRIMESTRE','PONDERA','AGLOMERADO','CONDICION_LABORAL'])
        datos_personas['PERIODO'] = datos_personas['ANO4'].astype(str) + 'TRIM' + datos_personas['TRIMESTRE'].astype(str)
        
        tipos = ['desempleo', 'empleo']
        selec_tipo = st.selectbox('Seleccione la tasa de empleo o desempleo', tipos)
        resumen = datos_personas.groupby('PERIODO', group_keys=False).apply(lambda grupo: calcular_tasa(grupo, selec_tipo)).reset_index(name='Tasa')

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(resumen['PERIODO'], resumen['Tasa'], marker='o', linestyle='-', color='tomato')
        ax.set_title(f'Tasa de {selec_tipo} en el tiempo - {nombre_aglomerado}')
        ax.set_ylabel('Tasa (%)')
        ax.set_xlabel('Periodo (Año + Trimestre)')
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)
        
    except FileNotFoundError:
        st.error('No se encontró el archivo especificado.')
    except TypeError:
        st.error('Error en los parametros de llamada de la función.')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 5.4 - - - - - - - - - - - - - - - - - - - - - - - - - - 

def informacion_ocupacion():
    """
    Muestra un gráfico de barras horizontales que representa la distribución de tipos de empleo
    (Estatal, Privada, Otro) por aglomerado, utilizando datos de ocupación.
    Raises:
        Exception: Si ocurre un error al procesar los datos o generar el gráfico.
        Warning: Si no hay datos válidos para mostrar.
        st.error: Si no se encuentran las columnas requeridas en el DataFrame.
    """
    ocupacion_principal = {
        1.0: 'Estatal',
        2.0: 'Privada',
        3.0: 'Otro',
    }

    try:
        df = pd.read_csv(PROCESSED_DATA_INDIVIDUAL, delimiter=';')
        
        # Verificación de columnas
        columnas_requeridas = ['PONDERA', 'PP04A', 'ESTADO', 'AGLOMERADO']
        for col in columnas_requeridas:
            if col not in df.columns:
                st.error(f"Columna requerida '{col}' no encontrada")

        # Conversión y limpieza
        df = df.dropna(subset=columnas_requeridas)
        df['PP04A'] = pd.to_numeric(df['PP04A'], errors='coerce')
        df = df[df['PP04A'].isin([1.0, 2.0, 3.0])]
        df = df[df['ESTADO'] == 1]  # Solo ocupados

        if df.empty:
            st.warning("No hay datos válidos")

        # Obtener el diccionario de aglomerados
        nombres_aglomerados = aglo_dict()

        # Procesamiento
        resultados = []
        for codigo, grupo in df.groupby('AGLOMERADO'):
            # Convertir código a string para coincidir con las claves del diccionario
            codigo_str = str(int(codigo))
            nombre_aglomerado = nombres_aglomerados.get(codigo_str, f"Aglomerado {codigo_str}")
            total = grupo['PONDERA'].sum()
            fila = {'Aglomerado': nombre_aglomerado, 'Total ocupados': total}
            
            for tipo_cod, tipo_nombre in ocupacion_principal.items():
                porcentaje = grupo[grupo['PP04A'] == tipo_cod]['PONDERA'].sum() / total * 100
                fila[tipo_nombre] = porcentaje
            
            resultados.append(fila)

        df_resultados = pd.DataFrame(resultados)

        # Visualización
        if not df_resultados.empty:
            # Preparamos los datos para el gráfico
            df_plot = df_resultados.set_index('Aglomerado')
            
            fig, ax = plt.subplots(figsize=(8, 10))  # Más alto para nombres

            # Gráfico
            df_plot[['Estatal', 'Privada', 'Otro']].plot.barh(
                stacked=True,
                ax=ax,
                color=['#3498db', '#2ecc71', '#e74c3c']
            )

            
              # Nombres en eje Y
            ax.set_xlabel("Porcentaje (%)")
            ax.set_ylabel("Aglomerado")
            ax.set_title("Distribución de tipos de empleo por aglomerado", fontsize=12, pad=10)
            ax.legend(title="Tipo de empleo", loc='lower right')
            ax.tick_params(axis='y', labelsize=8)

            plt.tight_layout()
            st.pyplot(fig)

            # Mostrar tabla de valores
            st.dataframe(df_resultados.style.format({'Total ocupados': '{:,.0f}', 
                                              'Estatal': '{:.1f}%', 
                                              'Privada': '{:.1f}%', 
                                              'Otro': '{:.1f}%'}))
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 5.5 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 5.5 - - - - - - - - - - - - - - - - - - - - - - - - - - 
def conseguir_data(arch):
    """
    Obtiene el año y trimestre mínimo y máximo presentes en el DataFrame.

    Parámetros:
    arch (pd.DataFrame): DataFrame que contiene las columnas 'ANO4' y 'TRIMESTRE'.

    Retorna:
    tuple: (año_máximo, trimestre_máximo, año_mínimo, trimestre_mínimo) si tiene éxito,
        o (None, None, None, None) en caso de error.
    Raises:
    Exception: Si ocurre un error al calcular las fechas.
    """
    try:
        anoact = arch['ANO4'].max()
        trimact = arch[arch['ANO4'] == anoact]['TRIMESTRE'].max()
        anoant = arch['ANO4'].min()
        trimant = arch[arch['ANO4'] == anoant]['TRIMESTRE'].min()
        return anoact, trimact, anoant, trimant
    except Exception as e:
        st.error(f"Error al calcular las fechas: {e}")
        return None, None, None, None

def conseguir_tasas(data):
    """
    Calcula las tasas de empleo y desempleo por aglomerado a partir de los datos filtrados.

    Parámetros:
    data (pd.DataFrame): DataFrame con datos individuales y las columnas 'ESTADO', 'AGLOMERADO' y 'PONDERA'.

    Retorna:
    pd.DataFrame: DataFrame con columnas 'Tasa de Empleo (%)' y 'Tasa de Desempleo (%)' para cada aglomerado.
                Devuelve DataFrame vacío si data es None o está vacío.
    """
    if data is None or data.empty:
        return pd.DataFrame() 

    # Filtrar población activa, ocupada y desocupada
    activos = data[data['ESTADO'].isin([1, 2])]
    ocupados = data[data['ESTADO'] == 1]
    desocupados = data[data['ESTADO'] == 2]

    # Agrupar por aglomerado y sumar ponderaciones
    activos_ag = activos.groupby('AGLOMERADO')['PONDERA'].sum()
    ocupados_ag = ocupados.groupby('AGLOMERADO')['PONDERA'].sum()
    desocupados_ag = desocupados.groupby('AGLOMERADO')['PONDERA'].sum()

    # Evitar división por cero
    activos_ag = activos_ag.replace(0, pd.NA)

    # Calcular tasas y llenar nulos con 0
    tasas = pd.DataFrame({
        'Tasa de Empleo (%)': (ocupados_ag / activos_ag * 100).round(2),
        'Tasa de Desempleo (%)': (desocupados_ag / activos_ag * 100).round(2)
    }).fillna(0)

    return tasas

def conseguir_comparacion(tasas_ant, tasas_act):
    """
    Combina y compara las tasas de empleo y desempleo entre dos períodos y añade coordenadas geográficas.

    Parámetros:
    tasas_ant (pd.DataFrame): DataFrame con tasas del período anterior, debe contener columna 'AGLOMERADO'.
    tasas_act (pd.DataFrame): DataFrame con tasas del período actual, debe contener columna 'AGLOMERADO'.

    Retorna:
    pd.DataFrame: DataFrame combinado con las tasas para ambos períodos y las coordenadas geográficas.
                Retorna DataFrame vacío si ocurre algún error o no hay datos para comparar.
    Raises:
    FileNotFoundError: Si no se encuentra el archivo de coordenadas.
    KeyError: Si hay un error al hacer el merge con las coordenadas.
    Exception: Si ocurre un error al cargar las coordenadas desde el archivo JSON.
    Warning: Si no hay tasas disponibles para comparar.
    st.error: Si hay un error al cargar las coordenadas.
    """
    if tasas_ant.empty or tasas_act.empty:
        st.warning("No hay tasas disponibles para comparar.")
        return pd.DataFrame()

    # Hacer merge entre tasas actuales y anteriores
    comparacion = pd.merge(tasas_act, tasas_ant, on='AGLOMERADO', how='inner', 
                        suffixes=('_act', '_ant'))

    try:
        # Cargar coordenadas de aglomerados desde archivo JSON
        with open(COORDS, "r", encoding="utf-8") as f:
            coords_json = json.load(f)

        if not isinstance(coords_json, dict):
            st.error("El archivo de coordenadas no tiene el formato esperado.")
            return pd.DataFrame()

        # Convertir JSON a DataFrame con coordenadas y nombres
        coords_df = pd.DataFrame([
            {
                "AGLOMERADO": int(nombre),
                "Nombre": valor["nombre"],
                "LAT": valor["coordenadas"][0],
                "LON": valor["coordenadas"][1]
            }
            for nombre, valor in coords_json.items()
        ])

        # Agregar coordenadas a la comparación
        comparacion = pd.merge(comparacion, coords_df, on="AGLOMERADO", how="left")
        return comparacion

    except FileNotFoundError:
        st.error(f"No se encontró el archivo de coordenadas: {COORDS}")
    except KeyError as e:
        st.error(f"Error en merge con coordenadas: columna no encontrada: {e}")
    except Exception as e:
        st.error(f"Error al cargar coordenadas: {e}")

    return pd.DataFrame()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 5.5 - - - - - - - - - - - - - - - - - - - - - - - - - -
def muestra_tasas_empleoydesempleo():
    """
    Muestra un mapa interactivo con la comparación de tasas de empleo y desempleo 
    entre el trimestre más antiguo y el más reciente disponibles en el archivo CSV.

    Parámetros:
    No recibe parámetros. Utiliza una ruta fija al archivo de datos (variable global).

    Salida:
    No retorna valores. Muestra directamente gráficos y mensajes en la interfaz Streamlit.

    Excepciones:
    - Muestra mensajes de error si no se puede cargar el archivo CSV.
    - Muestra advertencias si no hay datos o no se pueden determinar los períodos.
    - Captura y muestra errores al generar el mapa interactivo.
    """
    try:
        # Cargar datos procesados individuales
        arch = pd.read_csv(PROCESSED_DATA_INDIVIDUAL, sep=';')
    except Exception as e:
        st.error(f"No se pudo cargar el archivo de datos: {e}")
        return

    # Verificar que el archivo no esté vacío
    if arch is not None and not arch.empty:
        # Obtener año y trimestre actual y anterior
        ano_act, trim_act, ano_ant, trim_ant = conseguir_data(arch)
        if None in (ano_act, trim_act, ano_ant, trim_ant):
            st.warning("No se pudieron determinar los períodos de comparación.")
            return

        # Mostrar subtítulo con los trimestres comparados
        st.subheader(f"Datos de la EPH del T{trim_ant}/{ano_ant} y T{trim_act}/{ano_act}")

        # Filtrar los datos para ambos trimestres
        data_ant = arch[(arch['ANO4'] == ano_ant) & (arch['TRIMESTRE'] == trim_ant)]
        data_act = arch[(arch['ANO4'] == ano_act) & (arch['TRIMESTRE'] == trim_act)]

        if data_ant.empty or data_act.empty:
            st.warning("No hay datos disponibles para uno o ambos trimestres seleccionados.")
            return

        # Calcular tasas para cada período
        tasas_ant = conseguir_tasas(data_ant).reset_index()
        tasas_act = conseguir_tasas(data_act).reset_index()

        # Generar comparación entre trimestres
        dataframe_aglomerados = conseguir_comparacion(tasas_ant, tasas_act)
        if dataframe_aglomerados.empty:
            return

        # Selector de tipo de tasa
        tipo_tasa = st.radio("Seleccione la tasa a visualizar", ["Tasa de Empleo", "Tasa de Desempleo"])

        # Determinar columna y signo para el análisis
        columna = 'Tasa de Empleo (%)' if tipo_tasa == "Tasa de Empleo" else 'Tasa de Desempleo (%)'
        signo = 1 if tipo_tasa == "Tasa de Empleo" else -1

        # Calcular variación entre trimestres y definir color
        dataframe_aglomerados['variacion'] = signo * (
            dataframe_aglomerados[f'{columna}_act'] - dataframe_aglomerados[f'{columna}_ant']
        )
        dataframe_aglomerados['color'] = dataframe_aglomerados['variacion'].apply(
            lambda x: 'green' if x > 0 else 'red'
        )
        dataframe_aglomerados['valor'] = dataframe_aglomerados[f'{columna}_act']

        try:
            # Crear mapa con folium
            mapa = folium.Map(location=[-38, -63], zoom_start=4.3)
            for _, row in dataframe_aglomerados.iterrows():
                if pd.notna(row['LAT']) and pd.notna(row['LON']):
                    popup_text = (
                        f"{row['Nombre']} | {tipo_tasa}: {row['valor']:.2f}% | Variación: {row['variacion']:.2f}%"
                    )
                    folium.CircleMarker(
                        location=[row['LAT'], row['LON']],
                        radius=7,
                        color=row['color'],
                        fill=True,
                        fill_color=row['color'],
                        fill_opacity=0.8,
                        tooltip=row['Nombre'],
                        popup=popup_text
                    ).add_to(mapa)

            # Mostrar mapa en la app
            folium_static(mapa, width=700, height=500)

            # Leyenda del mapa
            st.markdown("""
            **Colores del mapa**:
            - :large_green_circle: Mejora respecto al período anterior  
            - :red_circle: Empeora respecto al período anterior
            """)
        except Exception as e:
            st.error(f"Error al generar el mapa: {e}")
    else:
        st.warning("El archivo está vacío o no se pudo cargar correctamente.")