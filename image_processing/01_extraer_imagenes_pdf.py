"""
Extraer imágenes contenidas en un archivo_pdf
"""
import fitz
from glob import glob
from PIL import Image

from utils import crear_directorio_si_no_existe
from utils import extraer_nombre_base

ruta_entrada = "../scanned_images/pdf_test"
ruta_salida = '../scanned_images/img_test'

# Funcionalidad central

def procesar_pdf(nombre_archivo, ruta_salida):
    nombre_base = extraer_nombre_base(nombre_archivo)
    archivo_pdf = fitz.open(nombre_archivo)

    # Se crea la ruta en la que se colocarán las imágenes
    crear_directorio_si_no_existe(f'{ruta_salida}/{nombre_base}')

    # Se guarda cada imagen del pdf
    for i, pagina in enumerate(archivo_pdf):
        imagenes = pagina.get_images()
        print(f"\tPágina {i}")

        for imagen in imagenes:
            xref = imagen[0]

            # Datos de la imagen
            imagen_base = archivo_pdf.extract_image(xref)
            bytes_imagen = imagen_base['image']
            extension = imagen_base['ext']

            # Guardar la imagen en un archivo
            archivo_img = f'{ruta_salida}/{nombre_base}/{i}.{extension}'
            with open(archivo_img, 'wb') as img:
                img.write(bytes_imagen)

# Programa principal
def main():
    for nombre_archivo in glob(f'{ruta_entrada}/*.pdf'):
        print(f'[+] Procesando: {nombre_archivo}')
        procesar_pdf(nombre_archivo, ruta_salida)


if __name__ == '__main__':
    main()
