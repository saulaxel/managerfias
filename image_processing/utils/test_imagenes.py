import unittest
import numpy as np

from imagenes import *

class TestImagenes(unittest.TestCase):
    ######################################################################
    def test_aplanar_una(self):
        test_image = np.array([
                [[1, 1, 1], [2, 2, 2]],
                [[3, 3, 3], [4, 4, 4]]
            ])
        expected_result = np.array([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])
        self.assertTrue(np.all(aplanar_una(test_image) == expected_result))

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
        self.assertTrue(np.all(aplanar_varias(test_images) == expected_result))

    ######################################################################
    def test_cargar(self):
        imagen = cargar('./imagen_prueba.png')
        expected_result = np.array([
                [[0, 0, 255], [0, 255, 0]],
                [[255, 0, 0], [255, 255, 255]]
            ])
        self.assertTrue(np.all(imagen == expected_result))
