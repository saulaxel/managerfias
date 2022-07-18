""" Redimensionar las imágenes a un tamaño conveniente """
import cv2

class Redimensionar:
    def __init__(self, width, height, inter=cv2.INTER_AREA):
        # Guarda el ancho y alto objetivo y el método para interpolación
        self.width = width
        self.height = height
        self.inter = inter

    def preprocesar(self, image):
        # Redimensionar la imagen al tamaño almacenado, ignorando la relación de
        # aspecto
        return cv2.resize(image, (self.width, self.height),
                          interpolation=self.inter)
