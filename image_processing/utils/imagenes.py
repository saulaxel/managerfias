
def aplanar(datos):
    # Convierte vectores tridimensionales en vectores unidimensionales
    n, alto, ancho, canales = datos.shape
    return datos.reshape(n, alto * ancho * canales)

def normalizar(datos):
    datos = datos.astype("float")
    minimo = datos.min()
    maximo = datos.max()
    datos = (datos - minimo) / (maximo - minimo)
    return datos
