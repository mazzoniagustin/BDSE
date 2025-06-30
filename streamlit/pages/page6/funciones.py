import matplotlib.pyplot as plt
import streamlit as st
import sys
import pandas as pd 
from pathlib import Path
import time
import plotly.express as px

current_dir = Path().resolve()
src_dir = current_dir.parents[2] / "src"

# Agrega src al sys.path (como string)
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))
    
from funcionalidad import *
from constantes import *

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 6.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 6.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 6.1 - - - - - - - - - - - - - - - - - - - - - - - - - -
def mostrar_educacion_por_nivel():
    """
    Muestra un gráfico de barras horizontales con la cantidad de personas según el nivel educativo alcanzado,
    para un año seleccionado por el usuario.
    Parameters
    ----------
    None
    Returns
    -------
    None
    Raises
    ------
    exception
        Si no se puede cargar el archivo procesado.
    Warning
        Si faltan columnas necesarias para el análisis.
    """
    try:
        df = pd.read_csv(PROCESSED_DATA_INDIVIDUAL, sep=";")
    except Exception as e:
        st.error(f"No se pudo cargar el archivo procesado: {e}")


    anios = sorted(df["ANO4"].dropna().unique())
    anio = st.selectbox("Seleccioná un año", anios, key="anio_1_6_1")
    df_filtrado = df[df["ANO4"] == anio]

    conteo = df_filtrado.groupby("NIVEL_ED_str")["PONDERA"].sum().reset_index()
    conteo.columns = ["Nivel educativo", "Cantidad"]
    conteo = conteo.sort_values(by="Cantidad")

    figura = px.bar(
        conteo,
        x="Cantidad",
        y="Nivel educativo",
        orientation="h",
        title=f"Nivel educativo alcanzado - Año {anio}",
        labels={"Cantidad": "Población estimada", "Nivel educativo": "Nivel educativo"}
    )

    st.plotly_chart(figura, use_container_width=True)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 6.2 - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 6.2 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 6.2 - - - - - - - - - - - - - - - - - - - - - - - - - -
def nivel_educativo_mas_comun_por_grupo():
    """
    Muestra la distribución proporcional del nivel educativo más frecuente por grupo etario.

    Returns
    -------
    None
        Muestra un gráfico con las proporciones por grupo etario y nivel educativo.
    Raises
    ------
    FileNotFoundError
        Si no se encuentra el archivo de datos procesados.
    TypeError
        Si hay un error en los parámetros de llamada de la función.
    Warning
        Si faltan columnas necesarias para el análisis.
    """
    try:
        datos_personas = pd.read_csv(PROCESSED_DATA_INDIVIDUAL, delimiter=';')

        columnas = {'CH06', 'NIVEL_ED_str', 'PONDERA'}
        if not columnas.issubset(datos_personas.columns):
            st.warning("Faltan columnas para este análisis.")

        
        datos_personas['EDAD'] = pd.to_numeric(datos_personas['CH06'], errors='coerce')
        datos_personas['PONDERA'] = pd.to_numeric(datos_personas['PONDERA'], errors='coerce')
        datos_personas['NIVEL_ED'] = datos_personas['NIVEL_ED_str'].fillna("Sin información.")
        
        grupos = [
            (20,30),
            (30,40),
            (40,50),
            (50,60),
            (60,105),
        ]
        
        seleccionar_grupo = st.multiselect('Seleccione uno o más grupos',options= grupos,default= grupos)
        
        if seleccionar_grupo == []:
            st.warning('Se debe seleccionar al menos un grupo.')
            st.stop()
        
        datos_personas['GRUPO_ETARIO'] = pd.NA

        for inf, sup in seleccionar_grupo:
            limite = f'{inf}-{sup}' # recorre la tupla y escribe los grupos en formato string
            cumple = (datos_personas['EDAD'] >= inf) & (datos_personas['EDAD'] < sup) # filtra con para seleccionar filas donde la edad este en el rango
            datos_personas.loc[cumple, 'GRUPO_ETARIO'] = limite # asigna las filas a la columna grupo_etario

        datos_personas = datos_personas.dropna(subset=['GRUPO_ETARIO' , 'PONDERA', 'NIVEL_ED'])

        conteos = (
            datos_personas.groupby(['GRUPO_ETARIO', 'NIVEL_ED'])['PONDERA']
            .sum()
            .reset_index(name='ponderado')
        )

        tabla = conteos.pivot(index='GRUPO_ETARIO', columns='NIVEL_ED', values='ponderado').fillna(0)
        proporciones = tabla.div(tabla.sum(axis=1), axis=0) * 100
        st.write("Distribución del nivel educativo por grupo etario")
        proporciones_redondeado = proporciones.round(2)
        st.dataframe(proporciones_redondeado.style.highlight_max(axis=1, color="#0f8500"))

        fig, ax = plt.subplots(figsize=(12, 7))
        proporciones.plot.bar(stacked=True, ax=ax, colormap='tab20')
        ax.set_ylabel('Porcentaje (%)')
        ax.set_xlabel('Grupo Etario')
        ax.set_title('Nivel educativo más común por grupo etario')
        plt.xticks(rotation=45)
        plt.legend(title='Nivel Educativo', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(fig)

    
    except FileNotFoundError:
        st.error('No se encontró el archivo especificado.')
    except TypeError:
        st.error('Error en los parametros de llamada de la función.')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 6.3 - - - - - - - - - - - - - - - - - - - - - - - - - - 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -AUX 6.3 - - - - - - - - - - - - - - - - - - - - - - - - - - 
def mostrar_aglo(aglomerado):
    """
    Muestra el nombre del aglomerado seleccionado.
    Parameters:
        aglomerado (int): Valor del aglomerado seleccionado.
    Returns:
        Mapeo a string con el nombre del aglomerado.
    """
    return f' {aglo_dict()[aglomerado]}'

def convertir(archivo_hogares, archivo_personas):
    """
    Convierte los datos de hogares y personas en un archivo CSV con el top 5 de aglomerados universitarios.
    Parameters:
        archivo_hogares (str): Ruta al archivo de datos de hogares procesados.
        archivo_personas (str): Ruta al archivo de datos de personas procesados.
    Returns:
        None
    """
    top_5 = top_5_aglomerados_universitarios(archivo_hogares, archivo_personas, ok = True)
    archivo_nuevo_csv = "Top 5 aglomerados universitarios.csv"

    with open(archivo_nuevo_csv, mode='w', newline='', encoding='utf-8') as nuevo_arch:
        escritor = csv.writer(nuevo_arch, delimiter=';')
        
        # Escribir encabezado
        escritor.writerow(["Aglomerado", "Porcentaje (%)"])
        
        # Escribir los 5 primeros formateados
        for codigo, porcentaje in top_5[:5]:
            escritor.writerow([mostrar_aglo(codigo), f"{porcentaje:.2f}"])
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 6.3 - - - - - - - - - - - - - - - - - - - - - - - - - -
def convertir_top5_csv():
    """
    Convierte el ranking de los 5 aglomerados con mayor porcentaje de hogares con 2 o más universitarios a un archivo CSV.
    Parameters
    ----------
    None
    Returns
    -------
    None
    Raises
    ------
    ValueError
        Si se espera un número pero se recibe otro dato.
    """
    try:
        st.subheader('Se convertirá el ranking de los 5 aglomerados con mayor porcentaje de hogares con 2 o más universitarios a un archivo CSV.')
        st.write('¿Desea continuar?')
        
        hacer = st.button('Continuar')
        
        if hacer:
            convertir(PROCESSED_DATA_HOGAR, PROCESSED_DATA_INDIVIDUAL)
            
            # Barra de progreso simulada
            barra_placeholder = st.empty()
            with barra_placeholder:
                barra = st.progress(0)
                for pct in range(0, 101):
                    time.sleep(0.02)
                    barra.progress(pct)
            barra_placeholder.empty()
            
            st.success('El archivo CSV con los 5 aglomerados con más universitarios se creó exitosamente.')
            
            # Botón para descargar el archivo recién creado
            with open("Top 5 aglomerados universitarios.csv", "rb") as file:
                st.download_button(
                    label="📥 Descargar CSV",
                    data=file,
                    file_name="top5_aglomerados.csv",
                    mime='text/csv'
                )
                
    except ValueError:
        st.error("Error: se esperaba un número pero se recibió otro dato.")



#- - - - - - - - - - - - - - - - - - - - - - - - - - - -MAIN 6.4 - - - - - - - - - - - - - - - - - - - - - - - - - -

def informacion_sobre_alfabetizacion():
    """
    Muestra un análisis de la alfabetización en Argentina, incluyendo porcentajes de personas 
    alfabetizadas e incapaces de leer y escribir.
    Parameters
    ----------
    None
    Returns
    -------
    None
    warning
        Si faltan columnas necesarias para el análisis.
    """
    # Cargar datos
    try:
        df = pd.read_csv(PROCESSED_DATA_INDIVIDUAL, sep=";")
    except Exception as e:
        st.error(f"No se pudo cargar el archivo procesado: {e}")

    # Verificación de columnas esenciales
    columnas_necesarias = {'ANO4', 'CODUSU', 'CH09', 'CH06', 'PONDERA'}
    if not columnas_necesarias.issubset(df.columns):
        st.warning("Error: Faltan columnas necesarias para el análisis.")
        return
    
    # Conversión a numérico y limpieza
    df = df.assign(
        ANO4 = pd.to_numeric(df['ANO4'], errors='coerce'),
        CH06 = pd.to_numeric(df['CH06'], errors='coerce'),
        CH09 = pd.to_numeric(df['CH09'], errors='coerce'),
        PONDERA = pd.to_numeric(df['PONDERA'], errors='coerce')
    ).dropna(subset=columnas_necesarias)
    
    # Filtrado: mayores de 6 años y valores válidos de alfabetización
    df = df[(df['CH06'] > 6) & (df['CH09'].isin([1, 2]))].copy()
    
    # Borro columnas repetidas que tengan el mismo codusu y el mismo anio.
    df= df.drop_duplicates(subset=['CODUSU', 'ANO4'], keep='first')
    
    # Cálculo de estadísticas ponderadas
    resultados = df.groupby(['ANO4', 'CH09'])['PONDERA'].sum().unstack()
    totales = df.groupby('ANO4')['PONDERA'].sum()
    
    # Cálculo de porcentajes
    resultados_porc = (resultados.div(totales, axis=0) * 100).round(2)
    



    #VISUALIZACION
    resultados_porc = resultados_porc.rename(columns={
        1: 'Alfabetizadas (%)',
        2: 'No alfabetizadas (%)'
    })
    
    # Crear tabla combinada
    tabla_combinada = resultados_porc.copy()
    tabla_combinada['Alfabetizadas (n)'] = resultados[1].astype(int)
    tabla_combinada['No alfabetizadas (n)'] = resultados[2].astype(int)


    # Reordenar columnas
    tabla_combinada = tabla_combinada[[
        'Alfabetizadas (%)', 
        'Alfabetizadas (n)',
        'No alfabetizadas (%)', 
        'No alfabetizadas (n)'
    ]]

    st.title("Alfabetización en Argentina")
    
    st.dataframe(
        tabla_combinada.style.format({
            'Alfabetizadas (%)': '{:,.2f}%',   
            'No alfabetizadas (%)': '{:,.2f}%', 
            'Alfabetizadas (n)': '{:,.0f}',     
            'No alfabetizadas (n)': '{:,.0f}'    
        })
    )