import streamlit as st 
from .funciones import edad_promedio_por_aglomerado
from .funciones import calcular_dependencia_demografica, media_mediana,mostrar_distribucion_edad_y_sexo
def pagina3():
    st.title("Características demográficas")
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 3.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    mostrar_distribucion_edad_y_sexo()
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 3.2 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    st.subheader("Edad promedio por aglomerado")
    edad_promedio_por_aglomerado()
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 3.3 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    calcular_dependencia_demografica()
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 3.4 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    media_mediana()