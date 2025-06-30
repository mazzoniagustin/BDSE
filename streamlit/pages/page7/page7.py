import streamlit as st 
import pandas as pd
from pathlib import Path
import sys
import matplotlib.pyplot as plt

current_dir = Path().resolve()
src_dir = current_dir.parent / "src"

# Agrega src al sys.path (como string)
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

from constantes import *


def pagina7():
    """
    Presenta en Streamlit un análisis de ingresos de hogares con 4 integrantes,
    comparando el ingreso total familiar con las líneas de indigencia y pobreza
    promedio trimestrales de la canasta básica.

    Pasos realizados:
    - Carga los datos de hogares y filtra por año y trimestre seleccionados.
    - Carga los valores mensuales de la canasta básica, filtra por trimestre y año,
    y calcula el promedio trimestral de las líneas de indigencia y pobreza.
    - Calcula la cantidad ponderada de hogares con 4 integrantes que están
    por debajo de cada línea.
    - Muestra los resultados ponderados en pantalla.

    No recibe parámetros ni retorna valores; funciona directamente sobre datos y
    presenta resultados en la app Streamlit.

    Nota:
    Requiere que las variables globales DATA_HOGAR y CANASTA contengan las rutas
    correctas a los archivos CSV de hogares y canasta básica, respectivamente.
    """

    st.title("Ingresos")
    st.subheader("Ingresos de hogares con 4 integrantes")

    # === Cargar datasets ===
    try:
        df_hogar = pd.read_csv(DATA_HOGAR, sep=';')
    except Exception as e:
        st.error(f"No se pudo cargar el archivo de hogares: {e}")
        return
    df_hogar = df_hogar[["ANO4", "TRIMESTRE", "IX_TOT", "ITF", "PONDERA"]]

    # === Selectbox para elegir año ===
    anos_disponibles = sorted(df_hogar["ANO4"].unique())
    anio = st.selectbox("Seleccioná el año", ["indique año"] + anos_disponibles)

    # === Selectbox para elegir trimestre (si ya se seleccionó año) ===
    if anio != "indique año":
        trimestres_disponibles = sorted(df_hogar[df_hogar["ANO4"] == anio]["TRIMESTRE"].unique())
        if trimestres_disponibles:
            trimestre = st.selectbox("Seleccioná el trimestre", ["indique trimestre"] + trimestres_disponibles)
            if trimestre == "indique trimestre":
                st.warning("Por favor seleccioná un trimestre válido.")
                trimestre = None
                return
        else:
            st.write("No hay trimestres disponibles para el año seleccionado.")
            trimestre = None
    else:
        st.write("Por favor seleccioná un año válido.")
        trimestre = None
        return


    # Filtrar hogares con 4 integrantes, año y trimestre seleccionados
    hogares_4 = df_hogar[
        (df_hogar["IX_TOT"] == 4) &
        (df_hogar["ANO4"] == anio) &
        (df_hogar["TRIMESTRE"] == trimestre)
    ]

    if hogares_4.empty:
        st.write("No hay hogares con 4 integrantes para el año y trimestre seleccionados.")
        return

    # Cargar datos de la canasta básica
    try:
        df_canasta = pd.read_csv(CANASTA)  # Por defecto separa por coma
    except Exception as e:
        st.error(f"No se pudo cargar el archivo de canasta básica: {e}")
        return
    df_canasta['fecha'] = pd.to_datetime(df_canasta['indice_tiempo'])

    # Definir meses por trimestre
    meses_por_trimestre = {
        1: [1, 2, 3],
        2: [4, 5, 6],
        3: [7, 8, 9],
        4: [10, 11, 12]
    }

    meses = meses_por_trimestre.get(trimestre, [])
    if not meses:
        st.error("Trimestre inválido seleccionado.")
        return

    canasta_trim = df_canasta[
        (df_canasta['fecha'].dt.year == anio) &
        (df_canasta['fecha'].dt.month.isin(meses))
    ]

    if canasta_trim.empty:
        st.warning("No hay datos de canasta básica para el año y trimestre seleccionados.")
        return
    # Promediar líneas de indigencia y pobreza para el trimestre
    cba_prom = canasta_trim['linea_indigencia'].mean()
    cbt_prom = canasta_trim['linea_pobreza'].mean()

    # Mostrar promedios con st.metric en columnas
    col1, col2 = st.columns(2)
    col1.metric("Promedio Línea Indigencia", f"{cba_prom:.2f}")
    col2.metric("Promedio Línea Pobreza", f"{cbt_prom:.2f}")

    hogares_indigencia = hogares_4[hogares_4["ITF"] < cba_prom]
    hogares_pobreza = hogares_4[hogares_4["ITF"] < cbt_prom]

    total_ponderado = hogares_4["PONDERA"].sum()
    indigencia_ponderada = hogares_indigencia["PONDERA"].sum()
    pobreza_ponderada = hogares_pobreza["PONDERA"].sum()

    porc_indigencia = (indigencia_ponderada / total_ponderado) * 100 if total_ponderado > 0 else 0
    porc_pobreza = (pobreza_ponderada / total_ponderado) * 100 if total_ponderado > 0 else 0

    st.markdown("### Resultados ponderados")
    col3, col4, col5 = st.columns(3)
    col3.metric("Total hogares (ponderado)", f"{total_ponderado:.0f}")
    col4.metric("Hogares bajo indigencia", f"{indigencia_ponderada:.0f}", f"{porc_indigencia:.2f}%")
    col5.metric("Hogares bajo pobreza", f"{pobreza_ponderada:.0f}", f"{porc_pobreza:.2f}%")
    