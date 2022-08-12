'''
Pruebas que son tardadas y/o no completamente automatizadas
'''
import unittest
import numpy as np
from os.path import exists
from os import remove

from utils.imagenes import *

class PruebaLargaImagenes(unittest.TestCase):
    ######################################################################
    def test_mostrar_hasta_tecla_presionada(self):
        imagen = np.array([
                [[  0,  0, 255], [  0, 255,   0]],
                [[255,  0,   0], [255, 255, 255]]
            ], dtype='uint8')
        mostrar_hasta_tecla_presionada('Prueba', imagen)

