import streamlit as st 
from .funciones import nivel_educativo_mas_comun_por_grupo,informacion_sobre_alfabetizacion,convertir_top5_csv, \
    mostrar_educacion_por_nivel

def pagina6():
    st.title("Educación")
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 6.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    st.subheader("Nivel educativo alcanzado")
    mostrar_educacion_por_nivel()
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 6.2 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    st.subheader("Nivel educativo más común por grupo etario")
    nivel_educativo_mas_comun_por_grupo()
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 6.3 - - - - - - - - - - - - - - - - - - - - - - - - - -
    convertir_top5_csv()
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 6.4 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    informacion_sobre_alfabetizacion()
    st.divider()