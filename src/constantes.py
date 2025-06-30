from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent
DATA_PATH = PROJECT_PATH / "files"
DATA_OUT_PATH = PROJECT_PATH / "data_out"
DATA_HOGAR = DATA_OUT_PATH / "usu_hogar.csv"
DATA_INDIVIDUAL = DATA_OUT_PATH / "usu_individual.csv"
PROCESSED_DATA_PATH = PROJECT_PATH / "processed_data"
PROCESSED_DATA_INDIVIDUAL = PROCESSED_DATA_PATH / "individual_procesado.csv"
PROCESSED_DATA_HOGAR = PROCESSED_DATA_PATH / "hogar_procesado.csv"
DATA_EPH = PROJECT_PATH / "data_EPH"
COORDS = DATA_EPH / "aglomerados_coordenadas.json"
CANASTA = DATA_EPH / "valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv"


