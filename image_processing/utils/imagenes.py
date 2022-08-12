import cv2
import numpy as np

def cargar(ruta: str):
    """
    Carga una imagen como un arreglo tridimensional
    """
    imagen = cv2.imread(ruta)
    return imagen


def guardar(ruta: str, imagen):
    """
    Guarda un arreglo tridimensional en un archivo de imagen
    """
    cv2.imwrite(ruta, imagen)


def aplanar_una(imagen):
    """
    Convierte una imagen (arreglo numpy de tamaño alto * ancho * número de canales de
    color) en un arreglo unidimensional
    """
    alto, ancho, canales = imagen.shape
    vector = imagen.reshape(alto * ancho * canales)
    return vector


def aplanar_varias(imagenes):
    """
    Convierte un arreglo de imágenes (arreglos numpy de tamaño alto * ancho *
    número de canales de color) en una lista de vectores unidimensionales
    """
    n, alto, ancho, canales = imagenes.shape
    vectores = imagenes.reshape(n, alto * ancho * canales)
    return vectores


def recortar(imagen, corte_vertical, corte_horizontal):
    '''
    Recibe una imagen (arreglo tridimensional) y hace un corte de acuerdo a los
    dos objetos slice (corte_horizontal y corte_vertical) que se pasan como
    parámetros
    '''
    return imagen[corte_vertical, corte_horizontal]


def redimensionar_uniformemente(imagen, razon):
    '''
    Recibe una imagen (arreglo tridimensional) y la redimensiona usando la razón
    indicada al llamar a la función.
    '''
    alto, ancho, canales = imagen.shape
    nuevo_alto = int(alto * razon)
    nuevo_ancho = int(ancho * razon)
    imagen = cv2.resize(imagen, (nuevo_alto, nuevo_ancho), interpolation=cv2.INTER_LINEAR)
    return imagen


def pegar_horizontalmente(*imagenes):
    '''
    Recibe varias imágenes y las pega horizontalmente para crear una sola imagen
    nueva
    '''
    pegada = np.concatenate(imagenes, axis=1)
    '''
    for mat in matrices_imagenes:
        log.debug(mat.shape)
    log.debug(horizontal.shape)
    '''
    return pegada


def mostrar_hasta_tecla_presionada(msg: str, imagen):
    '''
    Muestra la imagen con el título dado, solo hasta que se presione una tecla
    '''
    cv2.imshow(msg, imagen)
    cv2.waitKey()
    cv2.destroyAllWindows()

