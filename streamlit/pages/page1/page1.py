import streamlit as st
def pagina1():
    """
    Muestra una introducción a la Encuesta Permanente de Hogares (EPH) en la página principal.

    Presenta un texto explicativo sobre qué es la EPH, su importancia y dónde encontrar
    los datos oficiales en la página del INDEC.

    Se muestra el título, encabezado y el texto con formato markdown,
    incluyendo un enlace a la página oficial del INDEC.
    """
    que_es_eph = '''
→ LA :red-background[*ENCUESTA PERMANENTE DE HOGARES (EPH)*] ES UN PROGRAMA NACIONAL QUE, 
A PARTIR DE RELEVAMIENTOS EN DIFERENTES AGLOMERADOS URBANOS,  
DA A CONOCER LAS TENDENCIAS Y CARACTERÍSTICAS SOCIOECONÓMICAS DE LA POBLACIÓN ARGENTINA.

EL ACCESO A ESTA INFORMACIÓN SE ENCUENTRA EN LA PÁGINA OFICIAL DEL 
[INDEC](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos) DONDE SE PROPORCIONAN UN PAR DE ARCHIVOS 
(HOGAR E INDIVIDUAL) POR CADA TRIMESTRE DE DIFERENTES AÑOS DESDE EL 2016.
'''

    st.title(":bar_chart: BASE DE DATOS SOCIOECONOMICOS")
    st.header("¿Qué es la EPH?")
    st.markdown(que_es_eph)