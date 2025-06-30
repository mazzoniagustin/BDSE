import streamlit as st
from .funciones import *
from constantes import PROCESSED_DATA_HOGAR

def pagina4():
    st.title("CARACTERÍSTICAS DE LAS VIVIENDAS")
    anios = determinar_años(PROCESSED_DATA_HOGAR)
    option= st.selectbox("Seleccione un año (o todos) para explorar las características de las viviendas", ["Todos"] + anios)
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    st.subheader("Cantidad de viviendas por año")
    cant_viv_por_anio(option , anios)
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.2 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    st.subheader("Cantidad de viviendas por tipo")
    mostrar_grafico_torta_vivienda(option)
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.3 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    st.subheader("Material predominante por aglomerado")
    material_predominante_por_aglomerado(option, anios)
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.4 - - - - - - - - - - - - - - - - - - - - - - - - - - 

    st.subheader("Porcentaje de viviendas con baño dentro del hogar por aglomerado")
    banio_dentro_hogar_aglomerado (option, anios)
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.5 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    st.subheader("Evolución de la tenencia de la vivienda")
    evolucion_tenencia(option)
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.6 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    st.subheader("Cantidad de viviendas en villa por aglomerado")
    viviendas_en_villa_por_aglomerado(option,anios)
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 4.7 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    st.subheader("Porcentaje de viviendas con habitabilidad precaria")
    exportar_porcentaje_habitabilidad(option, anios)
    st.divider()
