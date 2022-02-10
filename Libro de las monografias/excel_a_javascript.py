from math import isnan
import pandas as pd

alfabeto = [chr(x) for x in range(65, 91)]


def sanear_datos(dato) -> str:
    if isinstance(dato, str):
        return dato.replace('"', '\\"')

    if isinstance(dato, float):
        if isnan(dato):
            return ''
        return str(int(dato))

    raise Exception('Tipo de dato no esperado en una columna')


for letra in alfabeto:
    with open('Lista Monografias.xlsx', 'rb') as f:
        data = pd.read_excel(f, sheet_name=letra)

    for row in data.itertuples():
        editorial = sanear_datos(row.editorial)
        num_serie = sanear_datos(row.num_serie)
        nombre = sanear_datos(row.nombre)

        clave = letra
        clave += sanear_datos(row.codigo)
        clave += sanear_datos(row.letra)
        clave += sanear_datos(row.orden)


        print(f'[MONOGRAFIA, "{clave}", "{nombre}"],')
