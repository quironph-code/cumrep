import pandas as pd


def normalizar_columnas(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    df = df.rename(columns={
        "fecha": "fecha",
        "codigo": "codigo",
        "cum": "cum",
        "precio": "precio",
        "cantidad": "cantidad",
        "valor total": "valor total",
        "valor_total": "valor total",
        "documento": "documento",
        "tipo": "tipo"
    })

    return df


def validar_columnas(df):

    columnas = [
        "fecha",
        "codigo",
        "cum",
        "precio",
        "cantidad",
        "valor total",
        "documento",
        "tipo"
    ]

    faltantes = [
        c for c in columnas
        if c not in df.columns
    ]

    return faltantes


def obtener_nit(tia, nit_manual):

    if tia == "MU":
        return "25001"

    elif tia == "DE":
        return "25"

    elif tia == "DI":
        return "11001"

    return nit_manual


def completar_nit(nit):

    return str(nit).zfill(12)