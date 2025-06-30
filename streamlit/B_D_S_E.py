import streamlit as st
st.set_page_config(page_title="B.D.S.E.",layout="wide",page_icon=":computer:")
from pathlib import Path
import sys


current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"

# Agrega src al sys.path (como string)
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))


# Importar módulos necesarios
from constantes import *


#IMPORTACION DE PAGINAS
from pages.page1 import page1
from pages.page2 import page2
from pages.page3 import page3
from pages.page4 import page4
from pages.page5 import page5
from pages.page6 import page6
from pages.page7 import page7


LOGO_URL_SMALL = "https://c.files.bbci.co.uk/A1F2/production/_115185414_1-1.jpg" 
st.sidebar.image(LOGO_URL_SMALL, use_container_width=True)

# --- Sidebar ---
st.sidebar.title("Menú")
pagina = st.sidebar.radio("Navegación", ["Inicio", "Carga de datos","Características demográficas",
                        "Características de la vivienda.","Actividad y empleo","Educación","Ingresos"])

match pagina:
    case "Inicio":
        page1.pagina1()
    case "Carga de datos":
        page2.pagina2()
    case "Características demográficas":
        page3.pagina3()
    case "Características de la vivienda.":
        page4.pagina4()
    case "Actividad y empleo":
        page5.pagina5()
    case "Educación":
        page6.pagina6()
    case "Ingresos":
        page7.pagina7()
