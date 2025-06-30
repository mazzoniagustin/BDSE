import streamlit as st
from pathlib import Path

def verificar_coherencia_archivos(archivos_nuevos):
    hogares = [Path(f).stem.lower().strip() for f in archivos_nuevos if "hogar" in f.lower()]
    individuos = [Path(f).stem.lower().strip() for f in archivos_nuevos if "individual" in f.lower()]

    faltantes = []

    for h in hogares:
        anio_trim = h.split('_')[-1]  # T220
        esperado = f"usu_individual_{anio_trim}".lower()
        if esperado not in individuos:
            anio = anio_trim[2:]
            trimestre = anio_trim[1]
            faltantes.append((anio, trimestre, esperado))

    for i in individuos:
        anio_trim = i.split('_')[-1]
        esperado = f"usu_hogar_{anio_trim}".lower()
        if esperado not in hogares:
            anio = anio_trim[2:]
            trimestre = anio_trim[1]
            faltantes.append((anio, trimestre, esperado))   
    if faltantes:
        for anio, trimestre, faltante in faltantes:
            st.warning(f"Falta el archivo {faltante} (sin importar extensión)")
        return False
    else:
        st.success("Chequeo exitoso, no se encontraron inconsistencias.")
        return True
    

def verificar_coherencia_archivos_existentes(carpeta):
    archivos_existentes = [f.name for f in carpeta.iterdir() if f.is_file() and 'usu_' in f.name.lower()]
    return verificar_coherencia_archivos(archivos_existentes)
