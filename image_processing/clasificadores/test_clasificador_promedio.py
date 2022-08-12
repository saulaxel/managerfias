import unittest
import utils.log as log
log.configurar_logger(nuevo_nivel_requerido=log.INFO)
import numpy as np
import os

from clasificadores.clasificador_promedio import *


class TestClasificadorPeomedio(unittest.TestCase):
    ######################################################################
    def test_entrenar_predecir(self):
        cp = ClasificadorPromedio()
        datos = np.array([
                [1, 2, 1, 2],
                [2, 1, 2, 1], # Promedio: 1.5

                [5, 4, 5, 4],
                [4, 5, 4, 5], # Promedio: 4.5

                [9, 8, 9, 8],
                [8, 9, 8, 9], # Promedio: 8.5

                [15, 16, 15, 16], # Promedio: 15.5
                [16, 15, 16, 15]
            ])
        etiquetas = [
                'primero',
                'primero',

                'segundo',
                'segundo',

                'tercero',
                'tercero',

                'cuarto',
                'cuarto',
            ]
        cp.entrenar(datos, etiquetas)

        datos = np.array([
                [1, 1, 1, 1],
                [2, 2, 2, 2],
                [2.5, 2.5, 2.5, 2.5],

                [3.5, 3.5, 3.5, 3.5],
                [4, 4, 4, 4],
                [5, 5, 5, 5],
                [6, 6, 6, 6],

                [7, 7, 7, 7],
                [8, 8, 8, 8],
                [9, 9, 9, 9],
                [10, 10, 10, 10],
                [11, 11, 11, 11],
                [11.5, 11.5, 11.5, 11.5],

                [12.5, 12.5, 12.5, 12.5],
                [13, 13, 13, 13],
                [14, 14, 14, 14],
                [15, 15, 15, 15],
                [16, 16, 16, 16],
            ])
        predicciones_esperadas = [
                'primero',
                'primero',
                'primero',

                'segundo',
                'segundo',
                'segundo',
                'segundo',

                'tercero',
                'tercero',
                'tercero',
                'tercero',
                'tercero',
                'tercero',

                'cuarto',
                'cuarto',
                'cuarto',
                'cuarto',
                'cuarto',
            ]

        self.assertEqual(cp.predecir(datos), predicciones_esperadas)


    ######################################################################
    def test_guardar_cargar(self):
        archivo = 'test-guardar-cargar.txt'
        promedios = {
            'a': 1.0,
            'b': 2.0,
            'c': 3.0
        }
        cantidades = {
            'a': 2,
            'b': 2,
            'c': 2
        }
        cp = ClasificadorPromedio(promedios, cantidades)

        cp.guardar(archivo)

        nuevo_cp = ClasificadorPromedio.cargar(archivo)
        promedios_recuperados = nuevo_cp.promedios
        cantidades_recuperadas = nuevo_cp.cantidades

        self.assertTrue(promedios.keys() == promedios_recuperados.keys() ==
                cantidades.keys() == cantidades_recuperadas.keys())

        for key in promedios:
            self.assertEqual(promedios[key], promedios_recuperados[key])
            self.assertEqual(cantidades[key], cantidades_recuperadas[key])

        os.remove(archivo)
