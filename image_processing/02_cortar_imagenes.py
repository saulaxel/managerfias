"""
Cortar la parte relevante de la imagen escaneada
"""
import cv2
import os
from glob import glob
from argparse import ArgumentParser

from utils import crear_directorio_si_no_existe
from utils import extraer_nombre_base

corte_horizontal = slice(0, 1774)
corte_vertical = slice(936, -1)

# Funcionalidad central

def guardar_recorte(nombre_archivo, ruta_archivo='.', ruta_salida='.'):
    ruta_completa = f'{ruta_archivo}/{nombre_archivo}'
    imagen = cv2.imread(ruta_completa)

    if imagen is None:
        raise EnvironmentError('No se pudo abrir la imagen')

    # Se corta la imagen
    imagen_cortada = imagen[corte_horizontal, corte_vertical]

    # Guardando resultados
    cv2.imwrite(f'{ruta_salida}/{nombre_archivo}', imagen_cortada)

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
            # y así sucesivamente. El orden lexicográfico es tiene relevancia
            # porque los números adyacentes son respectivamente en frente y el
            # reverso de la misma monografía, así que nos aseguramos de
            # preservar dicho orden con el sort()
            archivos.sort()

            base = extraer_nombre_base(raiz)
            nuevo_dir = f'{ruta_salida}/{base}'
            crear_directorio_si_no_existe(nuevo_dir)

            for nombre_archivo in archivos:
                guardar_recorte(nombre_archivo,
                                ruta_archivo=raiz,
                                ruta_salida=nuevo_dir)

if __name__ == '__main__':
    main()
