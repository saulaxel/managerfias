import unittest
import utils.log as log
import sys
log.configurar_logger(nuevo_nivel_requerido=log.INFO)

from io import StringIO
from contextlib import redirect_stdout

from identificar_sobrantes import *


class TestIdentificarSobrantes(unittest.TestCase):
    ######################################################################
    def test_elecciones_validas_son_actual_y_anterior(self):
        self.assertEqual(len(elecciones_validas(1)), 2)
        self.assertEqual(len(elecciones_validas(2)), 2)

    def test_elecciones_validas_solo_actual_al_inicio(self):
        self.assertEqual(len(elecciones_validas(0)), 1)

    ######################################################################
    def test_eliminar_eleccion_acepta_casos_validos(self):
        lista = [1, 2, 3]
        indice = 2

        eliminar_eleccion(lista, Eleccion.ACTUAL, indice)
        self.assertEqual(lista, [1, 2])

        lista = [3, 4, 5]
        indice = 2
        eliminar_eleccion(lista, Eleccion.ANTERIOR, indice)
        self.assertEqual(lista, [3, 5])

    def test_eliminar_eleccion_rechaza_eleccion_invalida(self):
        lista = [1, 2, 3]
        self.assertRaises(ValueError, eliminar_eleccion, lista, Eleccion.NINGUNA, 2)

    ######################################################################
    def test_obtener_eleccion_acepta_casos_validos(self):
        lista = [1, 2, 3]
        indice = 2
        elemento = obtener_eleccion(lista, Eleccion.ACTUAL, indice)
        self.assertEqual(elemento, 3)

        elemento2 = obtener_eleccion(lista, Eleccion.ANTERIOR, indice)
        self.assertEqual(elemento2, 2)

    def test_obtener_eleccion_rechaza_casos_invalidos(self):
        lista = [1, 2, 3]
        self.assertRaises(ValueError, obtener_eleccion, lista, Eleccion.NINGUNA, 2)

    ######################################################################
    def test_mostrar_elecciones(self):
        lista = ['0x1', '0x2', '0x3']
        todas = (Eleccion.ACTUAL, Eleccion.ANTERIOR)
        solo_actual = (Eleccion.ACTUAL,)
        indice = 1

        buf1 = StringIO()
        with redirect_stdout(buf1):
            mostrar_elecciones(lista, todas, indice)

        buf1.seek(0)
        res1 = buf1.read().lower()

        self.assertTrue(Eleccion.ACTUAL.name.lower() in res1)
        self.assertTrue(Eleccion.ANTERIOR.name.lower() in res1)
        self.assertTrue('0x2' in res1)
        self.assertTrue('0x1' in res1)
        self.assertFalse('0x3' in res1)

        buf2 = StringIO()
        with redirect_stdout(buf2):
            mostrar_elecciones(lista, solo_actual, indice)

        buf2.seek(0)
        res2 = buf2.read().lower()

        self.assertTrue(Eleccion.ACTUAL.name.lower() in res2)
        self.assertFalse(Eleccion.ANTERIOR.name.lower() in res2)
        self.assertTrue('0x2' in res2)
        self.assertFalse('0x1' in res2)

    ######################################################################
    def test_elegir_sobrante_acepta_elecciones_validas(self):
        with redirect_stdout(StringIO()): # Suprimir la impresión a la salida estándar

            # Guardamos el stdin antes de poner una entrada inyectada por
            # nosotros
            stdin_real = sys.stdin

            sys.stdin = StringIO('1\n') # La función elegir_sobrante que toma
                                        # entrada del usuario, usará esta cadena
                                        # en su lugar
            ret = elegir_sobrante((Eleccion.ACTUAL, Eleccion.ANTERIOR))
            self.assertEqual(ret, Eleccion.ACTUAL)

            sys.stdin = StringIO('2\n')
            ret = elegir_sobrante((Eleccion.ACTUAL, Eleccion.ANTERIOR))
            self.assertEqual(ret, Eleccion.ANTERIOR)

            sys.stdin = stdin_real

    def test_elegir_sobrante_regresa_ninguna_al_elegir_invalida(self):
        with redirect_stdout(StringIO()): # Suprimir la impresión a la salida estándar

            stdin_real = sys.stdin

            sys.stdin = StringIO('2\n')
            ret = elegir_sobrante((Eleccion.ACTUAL,))
            self.assertEqual(ret, Eleccion.NINGUNA)

            sys.stdin = StringIO('texto\n')
            ret = elegir_sobrante((Eleccion.ACTUAL, Eleccion.ANTERIOR))
            self.assertEqual(ret, Eleccion.NINGUNA)

            sys.stdin = stdin_real

    ######################################################################
    def test_orden_numerico(self):
        lista = ['2.txt', '2.aaa.txt', '22.txt', '1.txt', '11.txt']
        esperada = ['1.txt', '2.aaa.txt', '2.txt', '11.txt', '22.txt']
        self.assertEqual(sorted(lista, key=orden_numerico), esperada)
