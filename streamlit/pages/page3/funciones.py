import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import sys
from pathlib import Path
import plotly.express as px
import altair as alt

current_dir = Path().resolve()
src_dir = current_dir.parents[2] / "src"

# Agrega src al sys.path (como string)
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

from funcionalidad import aglo_dict
from constantes import *

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 3.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 3.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 
def asignar_grupo_edad(edad):
    """
        Asigna un grupo de edad basado en el valor de edad proporcionado.

    Args:
        edad (int): Edad de la persona.

    Returns:
        str: Grupo de edad en formato "inicio-fin".
        None: Si la edad es NaN.
    """
    if pd.isna(edad):
        return None
    for inicio in range(0, 100, 10):
        if inicio <= edad < inicio + 10:
            return f"{inicio}-{inicio + 9}"
    return "100+"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 3.1 - - - - - - - - - - - - - - - - - - - - - - - - - -
def mostrar_distribucion_edad_y_sexo():
    """
    Muestra un gráfico de barras dobles con la distribución de la población
    por grupos de edad (cada 10 años) y sexo, filtrado por año y trimestre.
    Raises:
        KeyError: Si falta una columna esperada en el archivo de datos.
        FileNotFoundError: Si no se encuentra el archivo de datos individuales.
    """

    try:
        df = pd.read_csv(PROCESSED_DATA_INDIVIDUAL, sep=";")

        # Menú de selección de año y trimestre
        anios = sorted(df["ANO4"].dropna().unique())
        anio = st.selectbox("Seleccioná un año", anios, key="anio_1_3_1") # se suma la key para evitar conflictos
        trimestres = sorted(df[df["ANO4"] == anio]["TRIMESTRE"].dropna().unique())
        trimestre = st.selectbox("Seleccioná un trimestre", trimestres, key="trim_1_3_1")

        df_filtrado = df[(df["ANO4"] == anio) & (df["TRIMESTRE"] == trimestre)]

        # Agrupar edades
        edades = list(range(0, 101, 10))
        rangos_edades = [f"{i}-{i+9}" for i in edades[:-1]] # Crea el rango exceptuando el último valor
        df_filtrado["grupo_edad"] = df_filtrado["CH06"].apply(asignar_grupo_edad)
        orden_edad = rangos_edades + ["100+"] 

        # Agrupar y sumar ponderadores
        agrupado = df_filtrado.groupby(["grupo_edad", "CH04_str"])["PONDERA"].sum()
        df_agrupado = agrupado.reset_index()

        # Gráfico de barras por edad y sexo
        figura = px.bar(
            df_agrupado,
            x="grupo_edad",
            y="PONDERA",
            color="CH04_str",
            barmode="group",
            category_orders={"grupo_edad": orden_edad},
            labels={"grupo_edad": "Grupo de edad", "PONDERA": "Población estimada"},
            title=f"Distribución de la población por edad y sexo - {anio} T{trimestre}"
        )
        st.plotly_chart(figura)
        
    except KeyError as e:
        st.error(f"Falta una columna esperada en el archivo: {e}")
    except FileNotFoundError:
        st.error("No se encontró el archivo de datos individuales.")
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 3.2 - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 3.2 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 3.2 - - - - - - - - - - - - - - - - - - - - - - - - - -
def edad_promedio_por_aglomerado():
    """
    Calcula y grafica la edad promedio por aglomerado para el último año y trimestre cargados.

    Returns
    -------
    None
        Muestra en consola la edad promedio por aglomerado, con su respectivo grafico.
    Raises:
    FileNotFoundError: Si no se encuentra el archivo de datos procesados.
    TypeError: Si hay un error en los parámetros de llamada de la función.
    Warning: Si faltan columnas necesarias en el DataFrame.
    """
    try:
        datos_personas = pd.read_csv(PROCESSED_DATA_INDIVIDUAL, delimiter=';')

        columnas_necesarias = {'ANO4', 'TRIMESTRE', 'CH06', 'AGLOMERADO', 'PONDERA'}
        if not columnas_necesarias.issubset(datos_personas.columns):
            st.warning("Faltan columnas necesarias para el análisis.")
            

        datos_personas['ANO4'] = pd.to_numeric(datos_personas['ANO4'], errors='coerce')
        datos_personas['TRIMESTRE'] = pd.to_numeric(datos_personas['TRIMESTRE'], errors='coerce')
        datos_personas['CH06'] = pd.to_numeric(datos_personas['CH06'], errors='coerce')
        datos_personas['PONDERA'] = pd.to_numeric(datos_personas['PONDERA'], errors='coerce')
        datos_personas['AGLOMERADO'] = datos_personas['AGLOMERADO'].astype(str)

        anios_disponibles = sorted(datos_personas['ANO4'].unique(), reverse=True)
        anio_seleccionado = st.selectbox("Seleccionar año", anios_disponibles)
        trimestre_seleccionado = datos_personas[datos_personas['ANO4'] == anio_seleccionado]['TRIMESTRE'].dropna().max()
        
        datos_filtrados = datos_personas[
            (datos_personas['ANO4'] == anio_seleccionado) & 
            (datos_personas['TRIMESTRE'] == trimestre_seleccionado)
        ]

        # Cálculo de edad promedio
        datos_filtrados = datos_filtrados.dropna(subset=['CH06','PONDERA','AGLOMERADO'])
        edades = (
            datos_filtrados
            .assign(producto=datos_filtrados['CH06'] * datos_filtrados['PONDERA'])
            .groupby('AGLOMERADO')
            .agg(suma=('producto', 'sum'), suma_pondera=('PONDERA', 'sum'))
        )
        edades['EDAD_PROMEDIO'] = edades['suma'] / edades['suma_pondera']
        edades = edades.sort_values(by='EDAD_PROMEDIO')

        st.write(f"Edad promedio por aglomerado - Año {anio_seleccionado} Trimestre {trimestre_seleccionado}")
        st.dataframe(edades[['EDAD_PROMEDIO']].rename(index=lambda x: aglo_dict().get(x, f"Aglomerado {x}")))

        edades.index = edades.index.map(lambda x: aglo_dict().get(x, f'Aglomerado {x}'))
        fig, ax = plt.subplots(figsize=(10, 8))
        edades['EDAD_PROMEDIO'].plot(kind='barh', color='cornflowerblue', ax=ax)
        ax.set_title(f'Edad promedio por aglomerado (Año {anio_seleccionado}, Trimestre {trimestre_seleccionado})')
        ax.set_xlabel('Edad promedio')
        ax.set_ylabel('Aglomerado')
        plt.tight_layout()
        st.pyplot(fig)

    except FileNotFoundError:
        st.error('No se encontró el archivo especificado.')
    except TypeError:
        st.error('Error en los parámetros de llamada de la función.')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 3.3 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 3.3 - - - - - - - - - - - - - - - - - - - - - - - - - - 
def mostrar_aglo(aglomerado):
    """
    Muestra el nombre del aglomerado seleccionado.
    Parameters:
        aglomerado (int): Valor del aglomerado seleccionado.
    Returns:
        Mapeo a string con el nombre del aglomerado.
    """
    return f' {aglo_dict()[aglomerado]}'

def mostrar_grafico_dependencia(evolucion):
    """
    Muestra un gráfico de barras de la evolución de la dependencia demográfica.
    
    Parameters:
        evolucion (DataFrame): DataFrame que contiene la evolución de la dependencia demográfica.
    Returns:
        chart: Gráfico de barras de Altair con la evolución.
    """
    evolucion2 = pd.DataFrame(evolucion)
    # Crear columna de periodo combinado
    evolucion2['Periodo'] = 'Año: ' + evolucion2['Año'].astype(str) + ', Trim: ' + evolucion2['Trimestre'].astype(str)
    
    # Crear gráfico de barras con Altair
    chart = alt.Chart(evolucion2).mark_line(point=True).encode(
        x=alt.X('Periodo:N', sort=None, title='Periodo'),
        y=alt.Y('Proporcion:Q', title='Proporción'),
        tooltip=['Periodo', 'Proporcion']
    ).properties(
        width=600,
        height=400,
        title='Evolución de Dependencia Demográfica'
    ).configure_axisX(
        labelAngle=0
    )
    
    return chart

def hacer_calculo(grupo):
    """
    Calcula la proporción de población inactiva sobre la activa en un grupo de datos.
    
    Parameters:
        grupo (DataFrame): DataFrame que contiene los datos del grupo.
    Returns:
        float: Proporción de población inactiva sobre la activa, multiplicada por 100.
        Si la población activa es 0, retorna 0.
    """
    pob_inactiva = grupo.loc[((grupo['CH06']> 0) & ((grupo['CH06']<=14) |  (grupo['CH06']>=65))), 'PONDERA'].sum()
    pob_activa = grupo.loc[((grupo['CH06']>=15) & (grupo['CH06']<=64)), 'PONDERA'].sum()
    return (pob_inactiva/pob_activa) * 100 if pob_activa != 0 else 0
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 3.3 - - - - - - - - - - - - - - - - - - - - - - - - - -
def calcular_dependencia_demografica():
    """
    Calcula y muestra la evolución de la dependencia demográfica por aglomerado, año y trimestre.
    Raises:
        FileNotFoundError: Si no se encuentra el archivo de datos procesados.
        ValueError: Si hay un error al convertir los datos a numéricos.
        Warning: Si faltan columnas requeridas en el DataFrame.
    """
    try:
        individuos = pd.read_csv(PROCESSED_DATA_INDIVIDUAL, delimiter=';', encoding='utf-8')
        columnas_necesarias = {'ANO4', 'TRIMESTRE', 'CH06', 'AGLOMERADO', 'PONDERA'}
        if not columnas_necesarias.issubset(individuos.columns):
            st.warning("Faltan columnas requeridas ('ANO4', 'TRIMESTRE', 'CH06', 'AGLOMERADO', 'PONDERA')")
            

        individuos['ANO4'] = pd.to_numeric(individuos['ANO4'], errors='coerce')
        individuos['TRIMESTRE'] = pd.to_numeric(individuos['TRIMESTRE'], errors='coerce')
        individuos['CH06'] = pd.to_numeric(individuos['CH06'], errors='coerce')
        individuos['PONDERA'] = pd.to_numeric(individuos['PONDERA'], errors='coerce')
        individuos['AGLOMERADO'] = individuos['AGLOMERADO'].astype(str)

        aglo_disponibles = (individuos['AGLOMERADO'].unique())
        aglo_seleccionado = st.selectbox("Seleccionar aglomerado", aglo_disponibles, key='1.3.3')
        

        
        if aglo_seleccionado:
            filtrar_hogar = individuos[(individuos ['AGLOMERADO'] == aglo_seleccionado)]
            # calcula la dependencia demografica
            depen_demografica = filtrar_hogar.groupby(['ANO4', 'TRIMESTRE']).apply (hacer_calculo).reset_index()
            # columnas del df a imprimir
            depen_demografica.columns = ['Año', 'Trimestre', 'Proporcion']
            depen_demografica= depen_demografica.sort_values(['Año','Trimestre']).reset_index(drop=True)
            # nombre del aglomerado
            nom_Aglo = mostrar_aglo(aglo_seleccionado)
            st.write (f'Evolucion del aglomerado llamado {nom_Aglo}')
            fig = mostrar_grafico_dependencia (depen_demografica)
            st.altair_chart(fig, use_container_width=True)
    except FileNotFoundError:
        st.error("Error: no se encontró uno de los archivos especificados.")
    except ValueError:
        st.error("Error: se esperaba un número pero se recibió otro dato.")


def media_mediana():
    """
    Calcula y muestra la media y mediana de la edad de la población por año y trimestre.

    Returns
    """
    try:
        # Cargar datos
        datos = pd.read_csv(PROCESSED_DATA_INDIVIDUAL, delimiter=';')
        
        # Verificar columnas
        columnas_necesarias = {'ANO4', 'TRIMESTRE', 'CH06', 'PONDERA'}
        if not columnas_necesarias.issubset(datos.columns):
            st.error("Faltan columnas necesarias en el archivo.")

        # Convertir tipos
        datos['ANO4'] = pd.to_numeric(datos['ANO4'], errors='coerce')
        datos['TRIMESTRE'] = pd.to_numeric(datos['TRIMESTRE'], errors='coerce')  # Corregido typo
        datos['CH06'] = pd.to_numeric(datos['CH06'], errors='coerce')
        datos['PONDERA'] = pd.to_numeric(datos['PONDERA'], errors='coerce')

        # Eliminar filas con valores nulos en columnas clave
        datos = datos.dropna(subset=['ANO4', 'TRIMESTRE', 'CH06', 'PONDERA'])

        # Calcular resultados
        resultados = []
        grupos = datos.groupby(['ANO4', 'TRIMESTRE'])

        for (anio, trimestre), grupo in grupos:
            # Media ponderada
            suma_edades = (grupo['CH06'] * grupo['PONDERA']).sum()
            total_pondera = grupo['PONDERA'].sum()
            
            if total_pondera == 0:  # Evitar división por cero
                continue
                
            media = suma_edades / total_pondera
            
            # Mediana ponderada
            grupo_ordenado = grupo.sort_values('CH06')
            pondera_acumulada = grupo_ordenado['PONDERA'].cumsum()
            mitad_peso = total_pondera / 2
            mediana = grupo_ordenado[pondera_acumulada >= mitad_peso]['CH06'].iloc[0]
            
            resultados.append({
                'ANO4': int(anio),
                'TRIMESTRE': int(trimestre),
                'media_edad': round(media, 2),
                'mediana_edad': int(mediana)
            })

        # Mostrar resultados
        if not resultados:
            st.warning("No hay datos válidos para mostrar.")

        df = pd.DataFrame(resultados).rename(columns={
            'ANO4': 'Año',
            'TRIMESTRE': 'Trimestre',
            'media_edad': 'Media',
            'mediana_edad': 'Mediana'
        })

        
        st.title("📊 Edad media y mediana por período")
        
        # Mostrar tabla
        st.dataframe(
            df.style
            .format({'Media': "{:.1f} años", 'Mediana': "{:.0f} años"})
            .highlight_max(subset=['Media'], color="#009b15")
            .highlight_min(subset=['Media'], color="#7c7c7c"),
            height=min(300, len(df)*35 + 40)
        )
        
        # Gráfico único simplificado
        plt.figure(figsize=(10, 5))
        
        # Configurar el gráfico
        plt.plot(df['Media'], color='#1f77b4', marker='o', linestyle='-', linewidth=2, label='Media')
        plt.plot(df['Mediana'], color='#ff7f0e', marker='s', linestyle='--', linewidth=2, label='Mediana')
        
        # Añadir títulos y etiquetas
        plt.title('Evolución de Edad Media vs Mediana', pad=20)
        plt.ylabel('Edad (años)')
        plt.xticks(rotation=45)
        
        # Añadir elementos de ayuda visual
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(loc='upper left')
        
        # Ajustar márgenes
        plt.tight_layout()
        
        # Mostrar en Streamlit
        st.pyplot(plt)
    except FileNotFoundError:
        st.error(f"Archivo no encontrado: {PROCESSED_DATA_INDIVIDUAL}")
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 3.4 - - - - - - - - - - - - - - - - - - - - - - - - - -