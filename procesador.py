import pandas as pd


def procesar_datos(
    df,
    fecha_inicio,
    fecha_final,
    tipo_campo
):

    # ----------------------------
    # FECHAS
    # ----------------------------

    df["fecha"] = pd.to_datetime(df["fecha"])

    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_final = pd.to_datetime(fecha_final)

    # ----------------------------
    # FILTRAR
    # ----------------------------

    df = df[
        (df["fecha"] >= fecha_inicio)
        &
        (df["fecha"] <= fecha_final)
    ]

    # ----------------------------
    # CREAR MES
    # ----------------------------

    df["mes"] = df["fecha"].dt.strftime("%m")

    # ----------------------------
    # ORDENAR
    # ----------------------------

    df = df.sort_values(
        by=["tipo", "mes", "cum"]
    )

    # ----------------------------
    # AGRUPAR
    # ----------------------------

    agrupado = df.groupby(
        ["tipo", "mes", "cum"]
    ).agg({
        "precio": ["min", "max"],
        "documento": ["min", "max"],
        "valor total": "sum",
        "cantidad": "sum"
    }).reset_index()

    agrupado.columns = [
        "tipo",
        "mes",
        "cum",
        "pmin",
        "pmax",
        "dmin",
        "dmax",
        "vtal",
        "cant"
    ]

    # ----------------------------
    # CAMPOS FIJOS
    # ----------------------------

    agrupado["p"] = 2

    agrupado["s"] = range(
        1,
        len(agrupado) + 1
    )

    agrupado["items"] = agrupado["s"]

    agrupado["o"] = 0

    agrupado["g"] = "04"

    agrupado["h"] = 0

    agrupado["j"] = 0

    agrupado["c"] = tipo_campo

    # ----------------------------
    # DIVIDIR CUM
    # ----------------------------

    agrupado[["cum1", "cum2"]] = (
        agrupado["cum"]
        .astype(str)
        .str.split("-", expand=True)
    )

    return agrupado