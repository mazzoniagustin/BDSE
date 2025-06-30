import streamlit as st
from .funciones import muestra_tasas_empleoydesempleo , evolucion_desempleo,informacion_ocupacion, mostrar_desocupacion_por_estudios
def pagina5():
    st.title("ACTIVIDAD Y EMPLEO")
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 5.1 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    st.subheader("DESOCUPACIÓN POR NIVEL DE ESTUDIOS")
    mostrar_desocupacion_por_estudios()
    st.divider()  
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 5.2 - INCISO 5.3- - - - - - - - - - - - - - - - - - - - - - - - - - 
    st.subheader("Evolución de Des/empleo")
    evolucion_desempleo()
    st.divider()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 5.4 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    informacion_ocupacion()
    st.divider()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -INCISO 5.5 - - - - - - - - - - - - - - - - - - - - - - - - - - 
    st.subheader("TASAS DE EMPLEO Y DESEMPLEO POR AGLOMERADO")
    muestra_tasas_empleoydesempleo()