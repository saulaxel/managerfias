"""
Cortar la parte relevante de la imagen escaneada
"""
import os
from glob import glob
from argparse import ArgumentParser

import utils.imagenes as imagenes
from utils import crear_directorio_si_no_existe
from utils import extraer_nombre_base

corte_vertical = slice(0, 1774)
corte_horizontal = slice(936, None) # None = Hasta el final

# Funcionalidad central

def cargar_recortar_y_guardar(nombre_archivo, ruta_archivo, ruta_salida):
    ruta_completa = f'{ruta_archivo}/{nombre_archivo}'
    imagen = imagenes.cargar(ruta_completa)

    if imagen is None:
        raise EnvironmentError('No se pudo abrir la imagen')

    imagen_cortada = imagenes.recortar(corte_vertical, corte_horizontal)

    imagen.guardar(f'{ruta_salida}/{nombre_archivo}', imagen_cortada)

# Programa principal
def main():
    ap = ArgumentParser()
    ap.add_argument('-e', '--ruta-entrada',
            default='../scanned_images/img')
    ap.add_argument('-s', '--ruta-salida',
            default='../scanned_images/img_cropped')

    args = vars(ap.parse_args())

    ruta_entrada = args['ruta_entrada']
    ruta_salida = args['ruta_salida']

    for raiz, directorios, archivos in os.walk(ruta_entrada):
        # Solo se toman en cuenta carpetas sin subdirectorios (el fondo
        # de la estructura de carpetas) para no tomar en cuenta la ruta que
        # principal (la que contiene al resto)
        if not directorios:
            # Los archivos están numerados 0.jpeg, 1.pjeg, 2.jpeg...,
            # y así sucesivamente. El orden lexicográfico tiene relevancia
            # porque los números adyacentes son respectivamente en frente y el
            # reverso de la misma monografía, así que nos aseguramos de
            # preservar dicho orden con el sort()
            archivos.sort()

            base = extraer_nombre_base(raiz)
            nuevo_dir = f'{ruta_salida}/{base}'
            if not crear_directorio_si_no_existe(nuevo_dir):
                print('El directorio ya existía')

            for nombre_archivo in archivos:
                cargar_recortar_y_guardar(nombre_archivo,
                                          ruta_archivo=raiz,
                                          ruta_salida=nuevo_dir)

if __name__ == '__main__':
    main()
