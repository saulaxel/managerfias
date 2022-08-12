'''
Clase que se entrena obteniendo el promedio de un conjunto de vectores de
característica. Luego, clasifica los nuevos vectores obteniendo la clase cuyo
promedio más se acerque al vector
'''
from typing import Dict
import numpy as np
from utils import log

class ClasificadorPromedio:
    def __init__(self, promedios: Dict[any, float]=None, cantidades: Dict[any, int]=None):
        if promedios is not None:
            self.__promedios = promedios
        else:
            self.__promedios = {}

        if cantidades is not None:
            self.__cantidades = cantidades
        else:
            self.__cantidades = {}

    def entrenar(self, datos, etiquetas):
        for dato, etiqueta in zip(datos, etiquetas):
            if etiqueta not in self.__cantidades:
                self.__promedios[etiqueta] = np.average(dato)
                self.__cantidades[etiqueta] = 1
            else:
                self.__promedios[etiqueta] += np.average(dato)
                self.__cantidades[etiqueta] += 1

        # Sacar el promedio de los promedios de las intensidades
        for clave in self.__cantidades.keys():
            self.__promedios[clave] /= self.__cantidades[clave]


    def predecir(self, X):
        predicciones = []
        promedios = np.average(X, axis=1)

        for promedio in promedios:

            mejor_prediccion = None
            minimo = float('inf')

            for clase in self.__cantidades.keys():
                error = abs(promedio - self.__promedios[clase])

                if error < minimo:
                    mejor_prediccion = clase
                    minimo = error

            predicciones.append(mejor_prediccion)

        return predicciones


    def guardar(self, nombre_archivo):
        with open(nombre_archivo, 'w') as f:
            for clase in self.__cantidades.keys():
                promedio = self.__promedios[clase]
                cantidad = self.__cantidades[clase]
                print(f'{clase} {promedio} {cantidad}', file=f)


    @classmethod
    def cargar(cls, nombre_archivo):
        nuevo = cls()
        with open(nombre_archivo) as f:
            for linea in f:
                clase, promedio, cantidad = linea.split()
                promedio = float(promedio)
                cantidad = int(cantidad)
                nuevo.__promedios[clase] = promedio
                nuevo.__cantidades[clase] = cantidad

        return nuevo

    @property
    def promedios(self):
        return self.__promedios.copy()

    @property
    def cantidades(self):
        return self.__cantidades.copy()
