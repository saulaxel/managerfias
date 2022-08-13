import unittest
import utils.log as log
log.configurar_logger(nuevo_nivel_requerido=log.INFO)

from cortar_imagenes import *

class PruebaLargaExtraerImagenes(unittest.TestCase):
    ######################################################################
    def test_extraer_imagenes(self):
        ruta_entrada = '../scanned_images/img_test'
        ruta_salida = '../scanned_images/img_test_output'
        procesar_imagens_en_subdirectorios(ruta_entrada, ruta_salida)
