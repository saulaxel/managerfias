"""
Algunas monografías se escanearon dos veces o más debido a pequeños errores.
Este script tiene la finalidad de identificarlas.

Se va a usar una heurística sencilla para este fin:
  * A partir de una muestra de imágenes ya separadas en frente y atrás, se
    calcula la media de los niveles de intensidad en ambas clases de imágenes.
  * Se usa la diferencia entre medias para clasificar el resto de imágenes
    en "de frente" y "detrás"
  * Las imágenes con número par deberían ser del frente y las impares deben ser
    la parte de atrás de una monografía. Si una imagen no concuerda con lo
    esperado, es probable que se haya duplicado. Se mostrarán ambas versiones al
    usuario para que elija la correcta.
"""
import cv2
import os
import os.path
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
    if not os.path.exists('03_promedios_frente_atras.txt'):
        # Si no se han caracterizado los promedios de niveles de intensidad
        # para frente y atrás, se procede a hacerlo
        ap = ArgumentParser()
        ap.add_argument('-e', '--ruta-entrada',
                default='../scanned_images/train_front_back')


    else:
        print('si');

    exit(1)

    args = vars(ap.parse_args())

    ruta_entrada = args['ruta_entrada']
    ruta_salida = args['ruta_salida']

    for raiz, directorios, archivos in os.walk(ruta_entrada):
        # Solo se toman en cuenta carpetas sin subdirectorios (el fondo
        # de la estructura de carpetas) para no tomar en cuenta la ruta que
        # contiene al resto
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
