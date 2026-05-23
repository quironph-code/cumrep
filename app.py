#streamlit run app.py con este se corre en proyecto_med100 por cnd venv\scripts\activate
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    normalizar_columnas,
    validar_columnas,
    obtener_nit
)

from procesador import procesar_datos

from generador_txt import generar_txt

# ---------------------------------
# CONFIGURACIÓN
# ---------------------------------

st.set_page_config(
    page_title="MED100MPRE",
    layout="wide"
)

st.title("📊 Generador MED100MPRE")

# ---------------------------------
# CARGAR ARCHIVO
# ---------------------------------

archivo = st.file_uploader(
    "Cargar Excel",
    type=["xlsx"]
)

# ---------------------------------
# FORMULARIO
# ---------------------------------

col1, col2 = st.columns(2)

with col1:

    fecha_inicio = st.date_input(
        "Fecha inicio"
    )

    tia = st.selectbox(
        "TIA",
        ["NI", "MU", "DE", "DI"]
    )

with col2:

    fecha_final = st.date_input(
        "Fecha final"
    )

    campo_c = st.selectbox(
        "Campo C",
        ["A", "B", "C", "D"]
    )
#["A:presentacion ccial", "B: unidad embalaje", "C: uni dispensacion", "D: uni min concent"]

# ---------------------------------
# NIT
# ---------------------------------

nit_manual = ""

if tia == "NI":

    nit_manual = st.text_input(
        "Ingresar NIT"
    )

nit = obtener_nit(
    tia,
    nit_manual
)

st.write(f"NIT utilizado: {nit}")

# ---------------------------------
# PROCESAR
# ---------------------------------

if archivo:

    df = pd.read_excel(archivo)

    df = normalizar_columnas(df)

    faltantes = validar_columnas(df)

    if faltantes:

        st.error(
            f"Faltan columnas: {faltantes}"
        )

        st.stop()

    # -----------------------------
    # PROCESAR
    # -----------------------------

    procesado = procesar_datos(
        df,
        str(fecha_inicio),
        str(fecha_final),
        campo_c
    )

    # -----------------------------
    # DASHBOARD
    # -----------------------------

    st.subheader("📈 Dashboard")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "CUM únicos",
            procesado["cum"].nunique()
        )

    with c2:
        st.metric(
            "Registros",
            len(procesado)
        )

    with c3:
        st.metric(
            "Valor total",
            f"${procesado['vtal'].sum():,.0f}"
        )

    # -----------------------------
    # ALERTAS
    # -----------------------------

    st.subheader("🚨 Alertas")

    promedio = procesado["pmax"].mean()

    altos = procesado[
        procesado["pmax"] > promedio * 2
    ]

    if len(altos) > 0:

        st.warning(
            f"{len(altos)} precios altos detectados"
        )

    else:

        st.success("Sin alertas")

    # -----------------------------
    # TABLA
    # -----------------------------

    st.subheader("📋 Datos procesados")

    st.dataframe(procesado)

    # -----------------------------
    # GRÁFICA
    # -----------------------------

    fig, ax = plt.subplots(figsize=(8,4))

    procesado.groupby("tipo")["vtal"].sum().plot(
        kind="bar",
        ax=ax
    )

    st.pyplot(fig)

    # -----------------------------
    # GENERAR TXT
    # -----------------------------

    if st.button("🚀 Generar TXT"):

        ruta = generar_txt(
            procesado,
            tia,
            nit,
            str(fecha_inicio),
            str(fecha_final)
        )

        st.success(
            f"Archivo generado: {ruta}"
        )

        with open(ruta, "rb") as file:

            st.download_button(
                label="⬇ Descargar TXT",
                data=file,
                file_name=ruta.split("/")[-1],
                mime="text/plain"
            )
