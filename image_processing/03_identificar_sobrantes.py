"""
Algunas monografías se escanearon dos veces o más debido a pequeños errores.
Este script tiene la finalidad de identificarlas.

Se va a usar una heurística sencilla para este fin:
  * A partir de una muestra de imágenes ya separadas en frente y atrás, se
    calcula la media de los niveles de promedios en ambas clases de imágenes.
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
import numpy as np
import re
import shutil

from glob import glob
from argparse import ArgumentParser
from imutils import paths
from sklearn.model_selection import train_test_split
from enum import Enum

from utils.sistema_archivos import crear_directorio_si_no_existe
from utils.sistema_archivos import extraer_nombre_base
from utils.sistema_archivos import extraer_extension
from utils import imagenes

from pyimagesearch.datasets.cargador_simple_datos import CargadorSimpleDatos

corte_horizontal = slice(0, 1774)
corte_vertical = slice(936, -1)

# Funcionalidad central
class ClasificadorPromedio:
    def __init__(self):
        self.promedios: dict[any, float] = {}
        self.cantidades: dict[any, int] = {}

    def entrenar(self, datos, etiquetas):
        for dato, etiqueta in zip(datos, etiquetas):
            if etiqueta not in self.cantidades:
                self.promedios[etiqueta] = np.average(dato)
                self.cantidades[etiqueta] = 1
            else:
                self.promedios[etiqueta] += np.average(dato)
                self.cantidades[etiqueta] += 1

        # Sacar el promedio de los promedios de las intensidades
        for clave in self.cantidades.keys():
            self.promedios[clave] /= self.cantidades[clave]

    def predecir(self, X):
        predicciones = []
        promedios = np.average(X, axis=1)

        for promedio in promedios:

            mejor_prediccion = None
            minimo = float('inf')

            for clase in self.cantidades.keys():
                error = abs(promedio - self.promedios[clase])

                if error < minimo:
                    mejor_prediccion = clase
                    minimo = error

            predicciones.append(mejor_prediccion)

        return predicciones

    def guardar(self, nombre_archivo):
        with open(nombre_archivo, 'w') as f:
            for clase in self.cantidades.keys():
                promedio = self.promedios[clase]
                cantidad = self.cantidades[clase]
                print(f'{clase} {promedio} {cantidad}', file=f)

    @classmethod
    def cargar(cls, nombre_archivo):
        nuevo = cls()
        with open(nombre_archivo) as f:
            for linea in f:
                clase, promedio, cantidad = linea.split()
                promedio = float(promedio)
                cantidad = int(cantidad)
                nuevo.promedios[clase] = promedio
                nuevo.cantidades[clase] = cantidad

        return nuevo

def redimensionar_uniformemente(imagen, razon):
    alto, ancho, canales = imagen.shape
    alto = int(alto * razon)
    ancho = int(ancho * razon)
    imagen = cv2.resize(imagen, (alto, ancho),
            interpolation=cv2.INTER_LINEAR)
    return imagen



class Eleccion(Enum):
    NINGUNA = 0
    ACTUAL = 1
    ANTERIOR = 2
    SIGUIENTE = 3

def elegir_sobrante(img_anterior: str, img_actual: str) -> Eleccion:
    matrices_imagenes = ()

    for nombre_imagen in (img_anterior, img_actual):
        if nombre_imagen is not None:
            imagen = imagenes.cargar(nombre_imagen)
            imagen = redimensionar_uniformemente(imagen, razon=0.3)
            matrices_imagenes += (imagen,)

    horizontal = np.concatenate(matrices_imagenes, axis=1)
    for mat in matrices_imagenes:
        print('[DEBUG] ', mat.shape)
    print('[DEBUG] ', horizontal.shape)
    cv2.imshow('Imagenes', horizontal)

    cv2.waitKey()
    cv2.destroyAllWindows()

    print("Elije la imagen a eliminar: ")
    print("1) Actual")
    print("2) Anterior")
    print("Cualquier otra cosa) Ninguna")
    eleccion = -1
    try:
        eleccion = int(input('> '))
    except ValueError:
        pass # Elección no se pudo convertir a entero


    if eleccion == 1:
        return Eleccion.ACTUAL
    if eleccion == 2:
        return Eleccion.ANTERIOR

    return Eleccion.NINGUNA


def orden_numerico(nombre_archivo):
    numero, *resto = re.split('[._]', nombre_archivo)
    return (int(numero), len(nombre_archivo))


def alternar_valor(actual, valor1, valor2):
    if actual == valor1:
        return valor2
    else:
        return valor1


FRENTE = 'front'
REVERSO = 'back'


# Programa principal
def main():
    """
    cp = ClasificadorPromedio()
    datos = np.array([
            [1, 2, 1, 2],
            [2, 1, 2, 1],
            [5, 4, 5, 4],
            [4, 5, 4, 5],
            [9, 8, 9, 8],
            [8, 9, 8, 9],
            [15, 16, 15, 16],
            [16, 15, 16, 15]
        ])
    etiquetas = ['primero', 'primero', 'segundo', 'segundo', 'tercero', 'tercero', 'cuarto', 'cuarto']

    X = np.array([
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3],
            [4, 4, 4, 4],
            [5, 5, 5, 5],
            [6, 6, 6, 6],
            [7, 7, 7, 7],
            [8, 8, 8, 8],
            [9, 9, 9, 9],
            [10, 10, 10, 10],
            [11, 11, 11, 11],
            [12, 12, 12, 12],
            [13, 13, 13, 13],
            [14, 14, 14, 14],
            [15, 15, 15, 15],
            [16, 16, 16, 16],
        ])
    cp.entrenar(datos, etiquetas)

    print(cp.predecir(X))

    cp.guardar('prueba.txt')

    nuevo_cp = ClasificadorPromedio.cargar('prueba.txt')
    print(cp.predecir(X))
    exit()
    """

    if not os.path.exists('03_promedios_frente_atras.txt'):
        # Si no se han caracterizado los promedios de niveles de promedios
        # para frente y atrás, se procede a hacerlo
        ap = ArgumentParser()
        ap.add_argument('-e', '--ruta-entrenamiento',
                default='../scanned_images/train_front_back')
        args = vars(ap.parse_args())

        # Carpetas dentro de la ruta de entrada, separados por clases
        rutas_imagenes = list(paths.list_images(args['ruta_entrenamiento']))

        # Cargar datos de entrenamiento
        (datos, etiquetas) = CargadorSimpleDatos().cargar(rutas_imagenes)

        # Preparar los datos
        datos = aplanar_imagenes(datos)

        # Particionar los datos usando 75% de los datos para entrenamiento y el restante
        # 25% para pruebas
        (trainX, testX, trainY, testY) = train_test_split(datos, etiquetas,
                test_size=0.25)

        print(f'{len(datos)=} {etiquetas=}')

        cp = ClasificadorPromedio()
        cp.entrenar(trainX, trainY)

        print(cp.predecir(testX))
        print(testY)

        cp.guardar('03_promedios_frente_atras.txt')

    else:
        # Ya está realizado el entrenamiento. Se procese a recorrer las
        # imágenes
        ap = ArgumentParser()
        ap.add_argument('-e', '--ruta-entrada',
                default='../scanned_images/img_cropped/')
        ap.add_argument('-s', '--ruta-salida',
                default='../scanned_images/img_no_repeated')
        args = vars(ap.parse_args())

        cp = ClasificadorPromedio.cargar('03_promedios_frente_atras.txt')

        ruta_entrada = args['ruta_entrada']
        ruta_salida = args['ruta_salida']

        contador_imagen = 0
        inicio = False
        for raiz, directorios, archivos in os.walk(ruta_entrada):
            # Solo se toman en cuenta carpetas sin subdirectorios (el fondo
            # de la estructura de carpetas) para no tomar en cuenta la ruta
            # carpeta principal

            if raiz == '../scanned_images/img_cropped/MX-M264N_20220701_140046':
                inicio = True

            if not inicio:
                continue

            if not directorios:
                # Los archivos están numerados 0.jpeg, 1.pjeg, 2.jpeg...,
                # y así sucesivamente. El orden lexicográfico es tiene relevancia
                archivos.sort(key=orden_numerico)

                base = extraer_nombre_base(raiz)

                actual = 0
                clasificacion_esperada = FRENTE

                # La lista de archivos va a ser filtrada, por lo que no se puede
                # recorrer mediante un for
                while actual < (largo := len(archivos)):
                    img = f'{raiz}/{archivos[actual]}'
                    img_anterior = None

                    # Construir rutas
                    if actual - 1 >= 0:
                        img_anterior = f'{raiz}/{archivos[actual - 1]}'

                    # Obtener la clasificación de la imagen
                    vector = imagenes.cargar(img)
                    vector = imagenes.aplanar_una(vector)

                    clasificacion = cp.predecir(vector)[0]

                    if clasificacion != clasificacion_esperada:
                        print('[DEBUG] Elegir sobrante entre:\n',
                              '[DEBUG]', actual, img, '\n',
                              '[DEBUG]', actual - 1, img_anterior)
                        sobrante = elegir_sobrante(img_anterior, img)

                        if sobrante == Eleccion.ANTERIOR:
                            # Tenemos que retroceder el índice si se eliminó algo previo
                            # para no saltarnos una imagen
                            actual -= 1
                            del archivos[actual]
                            clasificacion_esperada = alternar_valor(clasificacion_esperada, FRENTE, REVERSO)
                        elif sobrante == Eleccion.ACTUAL:
                            del archivos[actual]
                            actual -= 1
                            clasificacion_esperada = alternar_valor(clasificacion_esperada, FRENTE, REVERSO)

                    clasificacion_esperada = alternar_valor(clasificacion_esperada, FRENTE, REVERSO)
                    actual += 1

                if len(archivos) % 2 != 0:
                    print('[DEBUG] Número impar encontrado, eliminando el último lugar')
                    print('[DEBUG]', raiz)
                    del archivos[-1]
                    input()

                for nombre_imagen in archivos:
                    ruta_actual = f'{raiz}/{nombre_imagen}'
                    extension = extraer_extension(ruta_actual)
                    nueva_ruta = f'{ruta_salida}/{contador_imagen}.{extension}'
                    shutil.copy(ruta_actual, nueva_ruta)
                    contador_imagen += 1


if __name__ == '__main__':
    main()
