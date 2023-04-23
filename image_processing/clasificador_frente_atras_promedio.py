"""
Entrenamiento de un clasificador de imágenes que indica cuales son el 'frente'
de una monografía y cuales son la parte de 'atrás'.
  * A partir de una muestra de imágenes ya separadas en frente y atrás, se
    calcula la media de los niveles de promedios en ambas clases de imágenes.
  * Se usa la diferencia entre medias para clasificar el resto de imágenes
    en "de frente" y "detrás"
"""
from argparse import ArgumentParser
from utils import imagenes
from utils import log
from imutils import paths

from clasificadores import ClasificadorPromedio
from sklearn.model_selection import train_test_split
from pyimagesearch.datasets.cargador_simple_datos import CargadorSimpleDatos

ARCHIVO_SALIDA = 'clasificador_promedio.txt'

def entrenar_clasificador(ruta_entrenamiento, archivo_salida):

    # Carpetas dentro de la ruta de entrada, separados por clases
    rutas_imagenes = list(paths.list_images(ruta_entrenamiento))

    # Cargar datos de entrenamiento
    (datos, etiquetas) = CargadorSimpleDatos().cargar(rutas_imagenes)

    # Preparar los datos
    datos = imagenes.aplanar_varias(datos)

    # Particionar los datos usando 75% de los datos para entrenamiento y el restante
    # 25% para pruebas
    (trainX, testX, trainY, testY) = train_test_split(datos, etiquetas,
            test_size=0.25)

    log.msg(f'Datos originales:\n{len(datos)=}\n{etiquetas=}', nivel=log.DEBUG)

    cp = ClasificadorPromedio()
    cp.entrenar(trainX, trainY)

    log.msg('Predicción', str(cp.predecir(testX)), nivel=log.DEBUG)
    log.msg('Valor esperado:', str(testY), nivel=log.DEBUG)

    cp.guardar(archivo_salida)


def main():
    # Si no se han caracterizado los promedios de niveles de promedios
    # para frente y atrás, se procede a hacerlo
    ap = ArgumentParser()
    ap.add_argument('-e', '--ruta-entrenamiento',
            default='../scanned_images/train_front_back')
    args = vars(ap.parse_args())

    ruta_entrenamiento = args['ruta_entrenamiento']

    entrenar_clasificador(ruta_entrenamiento, ARCHIVO_SALIDA)


if __name__ == '__main__':
    main()
