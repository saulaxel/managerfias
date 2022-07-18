"""
Implementación de un perceptrón que se puede entrenar
"""
import numpy as np

class Perceptron:
    def __init__(self, N, alpha=0.1):
        # Inicializar la matriz de pesos y guardar la taza de aprendizaje
        self.W = np.random.randn(N + 1) / np.sqrt(N)
        self.alpha = alpha

    def funcion_escalon(self, x):
        return 1 if x > 0 else 0

    def entrenar(self, X, y, epocas=10):
        # Inserta una columna de unos como última entrada en la matriz de
        # característicos -- este truco permite tratar al sesgo como un
        # parámetro entrenable dentro de la matriz de pesos
        X = np.c_[X, np.ones((X.shape[0]))]

        for epoca in np.arange(0, epocas):
            for (x, objetivo) in zip(X, y):
                # Tomar el producto punto entre las características de entrada y
                # la matriz de pesos, entonces pasa este valor a través de
                # funcion_escalon para obtener la predicción
                prediccion = self.funcion_escalon(np.dot(x, self.W))

                # Solo realiza una actualización del peso si nuestra predicción
                # no coincide con el objetivo
                if prediccion != objetivo:
                    error = prediccion - objetivo

                    # Actualizar la matriz de pesos
                    self.W += -self.alpha * error * x

    def predecir(self, X, aniadir_sesgo=True):
        """Se calcula la clase predicha"""

        # Asegurarse de que la entrada sea una matriz
        X = np.atleast_2d(X)

        # Añadir el sesgo si se indica
        if aniadir_sesgo:
            # Insertar una columna de unos como la última entrada en la matriz
            # de características (sesgo)
            X = np.c_[X, np.ones((X.shape[0]))]

        # Tomar el producto punto entre las características de entrada y la
        # matriz de pesos, entonces pasar el valor a través de funcion_escalon
        return self.funcion_escalon(np.dot(X, self.W))
