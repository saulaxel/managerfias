import unittest
import tempfile
import os

from utils.sistema_archivos import *

class TestSistemaArchivos(unittest.TestCase):
    ######################################################################
    def test_extraer_nombre_base_maneja_casos_validos(self):
        self.assertEqual(extraer_nombre_base('/ruta/de/archivo.txt'), 'archivo')
        self.assertEqual(extraer_nombre_base('de/archivo.txt'), 'archivo')
        self.assertEqual(extraer_nombre_base('archivo.txt'), 'archivo')
        self.assertEqual(extraer_nombre_base('archivo'), 'archivo')
        self.assertEqual(extraer_nombre_base('1.2'), '1')

    def test_extraer_nombre_base_rechaza_casos_invalidos(self):
        self.assertRaises(ValueError, extraer_nombre_base, '')
        self.assertRaises(ValueError, extraer_nombre_base, None)

    ######################################################################
    def test_extraer_extension_maneja_casos_validos(self):
        self.assertEqual(extraer_extension('/ruta/de/archivo.txt'), 'txt')
        self.assertEqual(extraer_extension('de/archivo.txt'), 'txt')
        self.assertEqual(extraer_extension('archivo.txt'), 'txt')
        self.assertEqual(extraer_extension('1.2'), '2')

    def test_extraer_extension_rechaza_casos_invalidos(self):
        self.assertRaises(ValueError, extraer_extension, 'archivo')
        self.assertRaises(ValueError, extraer_extension, '')
        self.assertRaises(ValueError, extraer_extension, None)

    ######################################################################
    def test_crear_directorio_si_no_existe(self):
        nombre_archivo = next(tempfile._get_candidate_names())
        # El nombre temporal debe ser inexistente la primera vez, por lo que el
        # método habrá de generar 'True' (sí fue creado). Por su parte, la
        # segunda vez debe regresar 'False' (no se creo porque ya existía)
        self.assertEqual(crear_directorio_si_no_existe(nombre_archivo), True)
        self.assertEqual(crear_directorio_si_no_existe(nombre_archivo), False)
        os.rmdir(nombre_archivo)

    ######################################################################
    def test_guardar_bytes(self):
        datos_originales = b'0x10x20x30x4'
        archi = 'test-guardar-bytes.txt'
        guardar_bytes(archi, datos_originales)

        with open(archi, 'rb') as f:
            datos_recuperados = f.read()

        self.assertEqual(datos_originales, datos_recuperados)
        os.remove('test-guardar-bytes.txt')

