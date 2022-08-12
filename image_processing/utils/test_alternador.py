import unittest
import utils.log as log
log.configurar_logger(nuevo_nivel_requerido=log.INFO)

from utils.alternador import *


class TestClasificadorPeomedio(unittest.TestCase):
    ######################################################################
    def test_alternador(self):
        alternador = Alternador('cosa1', 'cosa2')
        self.assertEqual(alternador.valor_actual(), 'cosa1')

        alternador.cambiar_valor()
        self.assertEqual(alternador.valor_actual(), 'cosa2')

        alternador.cambiar_valor()
        self.assertEqual(alternador.valor_actual(), 'cosa1')

