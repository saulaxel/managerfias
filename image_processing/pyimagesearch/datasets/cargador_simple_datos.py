"""
Carga de imágenes
"""
import numpy as np
import cv2
import os


class CargadorSimpleDatos:
    def __init__(self, preprocesadores=None):
        self.preprocesadores = preprocesadores

        if self.preprocesadores is None:
            self.preprocesadores = []

    def load(self, rutas_imagenes, verboso=-1):
        datos = []
        etiquetas = []

        for i, ruta_imagen in enumerate(rutas_imagenes):
            # Cargar la imagen y extraer la etiqueta de clase asumiendo que
            # la ruta tiene el siguiente formato:
            # /ruta/hacia/imágenes/{clase}/{imagen}.algo
            imagen = cv2.imread(ruta_imagen)
            etiqueta = ruta_imagen.split(os.path.sep)[-2]

            # Pre-procesar
            for p in self.preprocesadores:
                imagen = p.preprocesar(imagen)

            # Se usará la imagen preprocesada como una "vector de
            # características", por lo que lo añadimos a la lista
            # correspondiente junto con su etiqueta correspondiente
            datos.append(imagen)
            etiquetas.append(etiqueta)

            # Si 'verboso' es mayor a cero, se puede usar para indicar mensajes
            # que indican el avance del procesamiento.
            # Se muestra el avance cada 'verboso' imágenes
            if verboso > 0 and i > 0 and (i + 1) & verboso == 0:
                print("[INFO] processed {}/{}".format(i + 1, len(rutas_imagenes)))

        return (np.array(datos), np.array(etiquetas))
