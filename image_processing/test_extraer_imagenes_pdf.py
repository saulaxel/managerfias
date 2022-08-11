import unittest
import utils.log as log

from extraer_imagenes_pdf import *

log.configurar_logger(nuevo_nivel_requerido=log.INFO)

class TestExtraerImagenes(unittest.TestCase):
    ######################################################################
    def test_abrir_pdf(self):
        abrir_pdf('./pdf-prueba.pdf')

    ######################################################################
    def test_obtener_imagenes(self):
        imagenes = list(obtener_imagenes(abrir_pdf('./pdf-prueba.pdf')))
        self.assertEqual(len(imagenes), 6)
