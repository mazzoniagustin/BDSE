# Integrantes del equipo : 

- Uceda Colombo, Juan Francisco
- Weber, Ezequiel
- Mazzoni, Marcos Agustin
- Libré, Nicolas
- Fernandez, Lucas

##  Deploy de la App:

  Accedé a la app online:
**[https://mazzoniagustin-bdse-app.streamlit.app](https://mazzoniagustin-bdse-app.streamlit.app)**

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mazzoniagustin-bdse-app.streamlit.app)


# Instrucciones para ejecutar el procesamiento de datos:

( Preferentemente se recomienda la instalacion de un entorno virtual, siendo este optimo para aislar la instalacion de las bibliotecas y paquetes necesarios para correr este proyecto. )

### Pasos a seguir para el procesamiento de datasets: 

Abrir la terminal desde el editor de texto que prefiera utilizar para correr los siguientes comandos: 

1. cd -ruta- | Posicionarse en el directorio donde se encuentre la carpeta del proyecto. Abrir el menu del boton derecho sobre el archivo descomprimido para tomar la ruta.

2. Acceder al siguiente link para la instalacion de la siguiente version de python: https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe. O verificar si cree tener instalada esa version de python en su maquina (python --version). 

2. python -m venv venv  |  Crea el entorno virtual.

3. En caso que su sistema operativo sea Windows: venv\Scripts\activate ; En caso de utilizar Linux/Mac: source venv/bin/activate  |  Activación.

4. pip install -r requirements.txt | Instala las dependencias.

Para correr las funciones del programa visualize el archivo individual.ipynb y hogar.ipynb. Dentro de cada uno vera el desarrollo del procesamiento de los datasets.

### Visualizacion de la aplicacion: 

( Con el entorno virtual activado, corremos los siguientes comandos. )

1. streamlit run streamlit/B_D_S_E.py  |  Lanza una apliacion web en una direccion local.

2. venv/Scripts/deactivate O venv/bin/deactivate  |  Desactiva el entorno virtual. ( Ejecutar una vez que termino de realizar pruebas en el proyecto. )

