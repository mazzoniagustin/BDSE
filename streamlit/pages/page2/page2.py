import streamlit as st
import altair as alt
import pandas as pd
from pathlib import Path
import sys
import time

current_dir = Path().resolve()
src_dir = current_dir.parents[2] / "src"

# Agrega src al sys.path (como string)
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))


from constantes import *
from funcionalidad import creacion_datasets, calcular_fechas_comparadas
from procesamiento import procesar_data
from .funciones import *


def pagina2():
    """
    Función principal para la página 2 de la aplicación Streamlit.

    Permite al usuario subir uno o más archivos (txt, csv, xls), controla si 
    existen archivos previos con el mismo nombre y pide confirmación para sobrescribirlos. 

    Tras confirmar la subida, guarda los archivos seleccionados en la carpeta de datos. 
    Luego verifica la coherencia entre archivos nuevos de hogares e individuos: para cada archivo 
    individual debe existir su correspondiente de hogares y viceversa.

    Si la verificación es exitosa, muestra un botón para actualizar la base de datos. 
    Al pulsarlo, ejecuta funciones para crear datasets y procesar datos, mostrando una barra de progreso.

    Finalmente, muestra un resumen de fechas disponibles en la base de datos y mensajes de éxito o advertencia
    según corresponda.

    En caso de no subir archivos, muestra la información de fechas de la base de datos ya existente.

    Usa módulos importados para la creación y procesamiento de datasets y para cálculos de fechas.

    """

    st.title("BASE DE DATOS ")

    # Mostrar estado actual de la base
    fechas = calcular_fechas_comparadas(PROCESSED_DATA_HOGAR, PROCESSED_DATA_INDIVIDUAL)
    if not fechas:
        st.error("No se encontraron datos procesados.")

    coherente = verificar_coherencia_archivos_existentes(DATA_PATH)
    if not coherente:
        st.warning("La base actual no está completa: hay pares hogar/individual faltantes.")
    else:
        st.info("Todos los pares de archivos hogar/individual están presentes.")

    carpeta_destino = DATA_PATH
    uploaded_files = st.file_uploader("Elegí uno o más archivos", accept_multiple_files=True, type=["txt", "csv", "xls"])

    if uploaded_files:
        st.write(f":file_folder: {len(uploaded_files)} archivo(s) seleccionados:")
        verificacion_sobreescritura = {}

        for uploaded_file in uploaded_files:
            new_file = carpeta_destino / uploaded_file.name
            if new_file.exists():
                st.warning(f":warning: El archivo {uploaded_file.name} ya existe.")
                sobrescribir = st.checkbox(f"¿Sobrescribir {uploaded_file.name}?", key=uploaded_file.name)
                verificacion_sobreescritura[uploaded_file.name] = sobrescribir
            else:
                st.write(f":white_check_mark: '{uploaded_file.name}' listo para guardar.")
                verificacion_sobreescritura[uploaded_file.name] = True

        if st.button("Confirmar subida"):
            archivos_aceptados = []

            for uploaded_file in uploaded_files:
                if verificacion_sobreescritura.get(uploaded_file.name, False):
                    ruta_archivo = carpeta_destino / uploaded_file.name
                    with open(ruta_archivo, "wb") as f:
                        f.write(uploaded_file.read())
                    st.success(f":floppy_disk: Archivo guardado: {uploaded_file.name}")
                    archivos_aceptados.append(uploaded_file.name)
                else:
                    st.info(f":x: No se guardó {uploaded_file.name} (no se autorizó sobreescritura).")

            if archivos_aceptados:
                ok = verificar_coherencia_archivos(archivos_aceptados)

                st.session_state["coherencia_ok"] = ok

                if not ok:
                    st.warning(" La verificación de coherencia falló. No se puede actualizar hasta corregir los archivos.")
                    return



    if st.session_state.get("coherencia_ok", False):
        if st.button("Actualizar base de datos"):
            actualizar_base()
            st.session_state["coherencia_ok"] = False



def actualizar_base():
    """ Ejecuta la creación y el procesamiento de datasets para ambos tipos. """
    st.write(":hourglass: Iniciando actualización de la base de datos...")

    with st.spinner("Creando datasets de individuos..."):
        creacion_datasets("I")
        st.success(":white_check_mark: Dataset de individuos creado.")

    with st.spinner("Procesando datos de individuos..."):
        procesar_data("I")
        st.success(":white_check_mark: Datos de individuos procesados.")

    with st.spinner("Creando datasets de hogares..."):
        creacion_datasets("H")
        st.success(":white_check_mark: Dataset de hogares creado.")

    with st.spinner("Procesando datos de hogares..."):
        procesar_data("H")
        st.success(":white_check_mark: Datos de hogares procesados.")

    barra_placeholder = st.empty()
    with barra_placeholder:
        barra = st.progress(0)
        for porcentaje in range(1, 101):
            time.sleep(0.01)
            barra.progress(porcentaje)
    barra_placeholder.empty()

    fechas = calcular_fechas_comparadas(PROCESSED_DATA_HOGAR, PROCESSED_DATA_INDIVIDUAL)
    st.subheader(f":green-background[BASE DE DATOS ACTUALIZADA: desde {fechas[1]}/{fechas[0]} hasta {fechas[3]}/{fechas[2]}] ")
    st.success(":white_check_mark: Actualización finalizada con éxito.")