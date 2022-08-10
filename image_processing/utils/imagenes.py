import cv2

def aplanar_una(imagen):
    """
    Convierte una imagen (arreglo numpy de tamaño alto * ancho * número de canales de
    color) en un arreglo unidimensional
    """
    alto, ancho, canales = imagen.shape
    vector = imagen.reshape(1, alto * ancho * canales)
    return vector


def aplanar_varias(imagenes):
    """
    Convierte un arreglo de imágenes (arreglos numpy de tamaño alto * ancho *
    número de canales de color) en una lista de vectores unidimensionales
    """
    n, alto, ancho, canales = imagenes.shape
    vectores = imagenes.reshape(n, alto * ancho * canales)
    return vectores


def cargar(nombre_archivo):
    """
    Carga una imagen como un arreglo tridimensional
    """
    imagen = cv2.imread(nombre_archivo)
    return imagen

