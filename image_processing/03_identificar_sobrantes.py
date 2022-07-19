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
from glob import glob
from argparse import ArgumentParser
from imutils import paths
from sklearn.model_selection import train_test_split

from utils.sistema_archivos import crear_directorio_si_no_existe
from utils.sistema_archivos import extraer_nombre_base
from utils.imagenes import aplanar
from utils.imagenes import normalizar

from pyimagesearch.datasets.cargador_simple_datos import CargadorSimpleDatos

corte_horizontal = slice(0, 1774)
corte_vertical = slice(936, -1)

# Funcionalidad central
class ClasificadorPromedio:
    def __init__(self):
        self.promedios: dict[float] = {}
        self.cantidades: dict[int] = {}

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


def cargar_imagen(nombre_archivo):
    imagen = cv2.imread(nombre_archivo)
    return imagen

def aplanar_unica_imagen(imagen):
    alto, ancho, canales = imagen.shape
    vector = imagen.reshape(1, alto * ancho * canales)
    return vector

def redimensionar_uniformemente(imagen, razon):
    alto, ancho, canales = imagen.shape
    alto = int(alto * razon)
    ancho = int(ancho * razon)
    imagen = cv2.resize(imagen, (alto, ancho),
            interpolation=cv2.INTER_LINEAR)
    return imagen


def elegir_sobrante(img_anterior, img_actual, img_siguiente):
    anterior, actual, siguiente = None, None, None
    imagenes = ()

    for nombre_imagen in (img_anterior, img_actual, img_siguiente):
        if nombre_imagen is not None:
            imagen = cargar_imagen(nombre_imagen)
            imagen = redimensionar_uniformemente(imagen, 0.25)
            imagenes += (imagen,)

    horizontal = np.concatenate(imagenes, axis=1)
    cv2.imshow(f'Imagenes {img_anterior} {img_actual} {img_siguiente}',
            horizontal)

    cv2.waitKey()
    cv2.destroyAllWindows()

    eleccion = int(input('> '))
    if eleccion == 0:
        return img_anterior
    if eleccion == 1:
        return img_actual
    if eleccion == 2:
        return img_siguiente

    return None





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
        datos = aplanar(datos)

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

        for raiz, directorios, archivos in os.walk(ruta_entrada):
            # Solo se toman en cuenta carpetas sin subdirectorios (el fondo
            # de la estructura de carpetas) para no tomar en cuenta la ruta
            # carpeta principal
            if not directorios:
                # Los archivos están numerados 0.jpeg, 1.pjeg, 2.jpeg...,
                # y así sucesivamente. El orden lexicográfico es tiene relevancia
                archivos.sort()

                base = extraer_nombre_base(raiz)

                actual = 0
                clasificacion_esperada = FRENTE

                # La lista de archivos va a ser filtrada, por lo que no se puede
                # recorrer mediante un for
                while actual < (largo := len(archivos)):
                    img = f'{raiz}/{archivos[actual]}'
                    img_anterior = None
                    img_siguiente = None

                    # Construir rutas
                    if actual - 1 >= 0:
                        img_anterior = f'{raiz}/{archivos[actual - 1]}'
                    if actual + 1 < largo:
                        img_siguiente = f'{raiz}/{archivos[actual + 1]}'

                    # Obtener la clasificación de la imagen
                    vector = cargar_imagen(img)
                    vector = aplanar_unica_imagen(vector)

                    clasificacion = cp.predecir(vector)[0]

                    if clasificacion != clasificacion_esperada:
                        sobrante = elegir_sobrante(img_anterior, img, img_siguiente)

                        if sobrante is None:
                            pass
                        elif sobrante == img_anterior:
                            del archivos[actual - 1]
                            actual -= 1
                        elif sobrante == img:
                            del archivos[actual]
                            actual -= 1
                        else:
                            del archivos[actual + 1]

                        # Tenemos que retroceder el índice si se eliminó algo previo
                        # para no saltarnos una imagen
                        if sobrante in (img_anterior, img):
                            actual -= 1


                    if clasificacion_esperada == FRENTE:
                        clasificacion_esperada = REVERSO
                    else:
                        clasificacion_esperada = FRENTE

                    actual + 1
                break


if __name__ == '__main__':
    main()
