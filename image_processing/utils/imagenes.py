import cv2

def aplanar_una(imagen):
    alto, ancho, canales = imagen.shape
    vector = imagen.reshape(1, alto * ancho * canales)
    return vector


def aplanar_varias(imagenes):
    # Convierte vectores tridimensionales en vectores unidimensionales
    n, alto, ancho, canales = datos.shape
    vectores = datos.reshape(n, alto * ancho * canales)
    return vectores


def cargar(nombre_archivo):
    imagen = cv2.imread(nombre_archivo)
    return imagen

