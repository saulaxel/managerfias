import unittest
import utils.log as log
log.configurar_logger(nuevo_nivel_requerido=log.INFO)

from identificar_sobrantes import *

class PruebaLargaIdentificarSobrantes(unittest.TestCase):
    ######################################################################
    def test_entrenar_clasificador(self):
        ruta_entrada = '../scanned_images/test_front_back'
        archivo_salida = '../scanned_images/test_classifier.txt'
        entrenar_clasificador(ruta_entrada, archivo_salida)

    ######################################################################
    def test_eliminar_sobrantes_carpetas(self):
        ruta_entrada = '../scanned_images/img_cropped_test'
        ruta_salida = '../scanned_images/img_cropped_test_output'
        cp = ClasificadorPromedio.cargar('./03_promedios_frente_atras.txt')
        eliminar_sobrantes_en_carpetas(cp, ruta_entrada, ruta_salida)
