"""
Extraer imágenes contenidas en un archivo_pdf
"""
import fitz  # Para manejar el pdf
from glob import glob
from PIL import Image

import utils.log as log
from utils import crear_directorio_si_no_existe
from utils import extraer_nombre_base
from utils import guardar_bytes
log.configurar_logger(log.DEBUG)

# Funciones adaptador para el manejo de imágenes
from collections import namedtuple
from typing import Iterable

Pdf = fitz.fitz.Document
Imagen = namedtuple('Imagen', ['ext', 'data'])


def abrir_pdf(nombre_archivo: str) -> Pdf:
    return fitz.open(nombre_archivo)


def obtener_imagenes(archivo_pdf: Pdf) -> Iterable[Imagen]:
    for i, pagina in enumerate(archivo_pdf):
        xrefs_imagenes = pagina.get_images()
        log.msg(f"Página {i}", nivel=log.DEBUG)

        for imagen in xrefs_imagenes:
            xref = imagen[0]

            # Datos de la imagen
            imagen_base = archivo_pdf.extract_image(xref)

            bytes_imagen = imagen_base['image']
            extension = imagen_base['ext']
            yield Imagen(ext=extension, data=bytes_imagen)


def procesar_pdf(nombre_archivo: str, ruta_salida: str) -> None:
    '''
    Obtiene todas las imágenes dentro del archivo y las guarda cada una por
    separado
    '''
    nombre_base = extraer_nombre_base(nombre_archivo)
    archivo_pdf = abrir_pdf(nombre_archivo)

    # Se crea la ruta en la que se colocarán las imágenes
    if not crear_directorio_si_no_existe(f'{ruta_salida}/{nombre_base}'):
        log.msg('El directorio ya existía')

    imagenes = obtener_imagenes(archivo_pdf)

    for i, imagen in enumerate(imagenes):
        archivo_img = f'{ruta_salida}/{nombre_base}/{i}.{imagen.ext}'
        guardar_bytes(nombre_archivo=archivo_img, bytes_a_guardar=imagen.data)


# Programa principal
def main() -> None:
    ap = ArgumentParser()
    ap.add_argument('-e', '--ruta-entrada',
            default='../scanned_images/pdf')
    ap.add_argument('-s', '--ruta-salida',
            default='../scanned_images/img')

    args = vars(ap.parse_args())

    ruta_entrada = args['ruta_entrada']
    ruta_salida = args['ruta_salida']

    for nombre_archivo in glob(f'{ruta_entrada}/*.pdf'):
        log.msg(f'Procesando: {nombre_archivo}', nivel=DEBUG)
        procesar_pdf(nombre_archivo, ruta_salida)


if __name__ == '__main__':
    main()
