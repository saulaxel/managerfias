
import unittest
import utils.log as log
log.configurar_logger(nuevo_nivel_requerido=log.INFO)

from extraer_imagenes_pdf import *

class PruebaLargaExtraerImagenes(unittest.TestCase):
    ######################################################################
    def test_extraer_imagenes(self):
        ruta_entrada = '../scanned_images/pdf_test'
        ruta_salida = '../scanned_images/pdf_test_output'
        extraer_imagenes_pdf(ruta_entrada, ruta_salida)
