import os


from utils import completar_nit


def generar_txt(
    df,
    tia,
    nit,
    fecha_inicio,
    fecha_final,
    ruta="reportes"
):

    if not os.path.exists(ruta):
        os.makedirs(ruta)

    # ---------------------------------
    # TOTALES
    # ---------------------------------

    sui = len(df)

    cuc = df["cum"].nunique()

    nit_archivo = completar_nit(nit)

    fecha_archivo = (
        fecha_final
        .replace("-", "")
    )

    nombre = (
        f"MED100MPRE"
        f"{fecha_archivo}"
        f"{tia}"
        f"{nit_archivo}.txt"
    )

    ruta_completa = os.path.join(
        ruta,
        nombre
    )

    # ---------------------------------
    # CREAR TXT
    # ---------------------------------

    with open(
        ruta_completa,
        "w",
        encoding="utf-8"
    ) as f:

        # CABECERA

        cabecera = (
            f"1|{tia}|{nit}|"
            f"{fecha_inicio}|"
            f"{fecha_final}|"
            f"{sui}|{cuc}"
        )

        f.write(cabecera + "\n")

        # DETALLE

        total = len(df)

        for i, row in enumerate(df.itertuples(), start=1):

            linea = (
                f"{row.p}|"
                f"{row.s}|"
                f"{row.items}|"
                f"{row.o}|"
                f"{row.mes}|"
                f"{row.p}|"
                f"{row.tipo}|"
                f"{row.g}|"
                f"{row.o}|"
                f"{row.h}|"
                f"{row.j}|"
                f"{row.cum1}|"
                f"{row.cum2}|"
                f"{row.c}|"
                f"{row.pmin}|"
                f"{row.pmax}|"
                f"{row.vtal}|"
                f"{row.cant}|"
                f"{row.dmin}|"
                f"{row.dmax}"
            )

            if i < total:
                f.write(linea + "\n")
            else:
                f.write(linea)

    return ruta_completa