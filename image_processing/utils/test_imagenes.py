import unittest
import numpy as np
from os.path import exists
from os import remove

from utils.imagenes import *

class TestImagenes(unittest.TestCase):
    ######################################################################
    def test_aplanar_una(self):
        test_image = np.array([
                [[1, 1, 1], [2, 2, 2]],
                [[3, 3, 3], [4, 4, 4]]
            ])
        expected_result = np.array([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])
        self.assertTrue(np.array_equal(aplanar_una(test_image), expected_result))

    def test_aplanar_una_acepta_un_solo_pixel(self):
        imagen = np.array([[[1, 1, 1]]])
        esperado = np.array([1, 1, 1])
        self.assertTrue(np.array_equal(aplanar_una(imagen), esperado))

    ######################################################################
    def test_aplanar_varias(self):
        test_images = np.array([
                [
                    [[1, 1, 1], [2, 2, 2]],
                    [[3, 3, 3], [4, 4, 4]]
                ],
                [
                    [[5, 5, 5], [6, 6, 6]],
                    [[7, 7, 7], [8, 8, 8]]
                ],
                [
                    [[9, 9, 9], [10, 10, 10]],
                    [[11, 11, 11], [12, 12, 12]]
                ],
                [
                    [[13, 13, 13], [14, 14, 14]],
                    [[15, 15, 15], [16, 16, 16]]
                ],
            ])
        expected_result = np.array([
                [ 1,  1,  1,  2,  2,  2,  3,  3,  3,  4,  4,  4],
                [ 5,  5,  5,  6,  6,  6,  7,  7,  7,  8,  8,  8],
                [ 9,  9,  9, 10, 10, 10, 11, 11, 11, 12, 12, 12],
                [13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16]
            ])
        self.assertTrue(np.array_equal(aplanar_varias(test_images), expected_result))

    ######################################################################
    def test_cargar(self):
        imagen = cargar('utils/imagen_prueba.png')
        expected_result = np.array([
                [[0, 0, 255], [0, 255, 0]],
                [[255, 0, 0], [255, 255, 255]]
            ])
        self.assertTrue(np.array_equal(imagen, expected_result))


    ######################################################################
    def test_guardar(self):
        imagen = np.array([
                [[0, 0, 255], [0, 255, 0]],
                [[255, 0, 0], [255, 255, 255]]
            ])
        ruta = 'utils/imagen_prueba_guardado.png'
        self.assertFalse(exists(ruta))
        guardar(ruta, imagen)
        self.assertTrue(exists(ruta))

        remove(ruta)

    ######################################################################
    def test_recortar_maneja_puntos(self):
        imagen = np.array([
                [[0, 0, 255], [0, 255, 0]],
                [[255, 0, 0], [255, 255, 255]]
            ])

        punto_ver, punto_hor = slice(0, 1), slice(0, 1)
        resultado1 = recortar(imagen, punto_ver, punto_hor)
        esperado1 = np.array([[[0, 0, 255]]])
        self.assertTrue(np.array_equal(resultado1, esperado1))

        punto2_ver, punto2_hor = slice(1, 2), slice(1, 2)
        resultado2 = recortar(imagen, punto2_ver, punto2_hor)
        esperado2 = np.array([[[255, 255, 255]]])
        self.assertTrue(np.array_equal(resultado2, esperado2))

    def test_recortar_maneja_lineas(self):
        imagen = np.array([
                [[0, 0, 255], [0, 255, 0]],
                [[255, 0, 0], [255, 255, 255]]
            ])

        columna_ver, columna_hor = slice(0, 2), slice(0, 1)
        resultado3 = recortar(imagen, columna_ver, columna_hor)
        esperado3 = np.array([
                [[0, 0, 255]],
                [[255, 0, 0]]
            ])
        self.assertTrue(np.array_equal(resultado3, esperado3))

        fila_ver, fila_hor = slice(0, 1), slice(0, 2)
        resultado4 = recortar(imagen, fila_ver, fila_hor)
        esperado4 = np.array([
                [[0, 0, 255], [0, 255, 0]]
            ])
        self.assertTrue(np.array_equal(resultado4, esperado4))

    def test_recortar_imagen_completa(self):
        imagen = np.array([
                [[0, 0, 255], [0, 255, 0]],
                [[255, 0, 0], [255, 255, 255]]
            ])

        completa_ver, completa_hor = slice(0, None), slice(0, None)
        resultado5 = recortar(imagen, completa_ver, completa_hor)
        esperado5 = np.array([
                [[0, 0, 255], [0, 255, 0]],
                [[255, 0, 0], [255, 255, 255]]
            ])
        self.assertTrue(np.array_equal(resultado5, esperado5))

    ######################################################################
    def test_redimensionar_uniformemente(self):
        imagen = np.array([
                [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
            ], dtype='uint8')
        nueva = redimensionar_uniformemente(imagen, 0.5)

    ######################################################################
    def test_pegar_horizontalmente(self):
        imagen1 = np.array([
                [[1, 1, 1], [1, 1, 1]],
                [[1, 1, 1], [1, 1, 1]],
            ], dtype='uint8')
        imagen2 = np.array([
                [[2, 2, 2], [2, 2, 2]],
                [[2, 2, 2], [2, 2, 2]],
            ], dtype='uint8')

        esperada = np.array([
                [[1, 1, 1], [1, 1, 1], [2, 2, 2], [2, 2, 2]],
                [[1, 1, 1], [1, 1, 1], [2, 2, 2], [2, 2, 2]],
            ], dtype='uint8')

        resultado = pegar_horizontalmente(imagen1, imagen2)
        self.assertTrue(np.array_equal(resultado, esperada))

