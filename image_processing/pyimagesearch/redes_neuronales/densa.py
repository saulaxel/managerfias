"""
Implementación en python puro de una red neuronal densa y con función de
activación sigmoide
"""
import numpy as np
from numpy.random import randn

class Densa:
    def __init__(self, capas, alpha=0.1, pesos=None):
        # Lista de matrices de pesos, la arquitectura de red y guardar la
        # arquitectura de red y taza de aprendizaje
        self.pesos = []
        self.capas = capas
        self.alpha = alpha

        if pesos is None:
            # Si no se recibieron los pesos como parámetro, se inicializan de
            # forma aleatoria

            # Se recorre desde el índice de la primera capa, pero dejamos sin
            # procesar las últimas dos capas
            for i in np.arange(0, len(capas) - 2):

                # Se conecta la cantidad de nodos que corresponde a cada capa,
                # añadiendo un nodo extra para el sesgo
                pesos = randn(capas[i] + 1, capas[i + 1] + 1)
                self.pesos.append(pesos / np.sqrt(capas[i]))

            # Las últimas dos capas son un caso especial donde las conexiones de
            # entrada necesitan el término de sesgo pero la salida no lo
            # necesita
            pesos = randn(capas[-2] + 1, capas[-1])
            self.pesos.append(pesos / np.sqrt(capas[-2]))
        else:
            # Si se reciben los pesos, simplemente se asignan a las posiciones
            # requeridas. Los pesos vienen en vectores de una dimensión en lugar
            # de en una matriz, por lo que se re-dimensionan antes de guardarse
            for i in np.arange(0, len(capas) - 2):
                pesos = pesos[i].reshape(capas[i] + 1, capas[i + 1] + 1)
                self.pesos.append(pesos)

            pesos = pesos[-1].reshape(capas[-2] + 1, capas[-1])
            self.pesos.append(pesos)

    def __repr__(self):
        """Se muestra la arquitectura de red"""
        return "RedNeuronalDensa: {}".format(
            "-".join(str(L) for L in self.capas))

    def sigmoide(self, x):
        """Calcula la función de activación sigmoide para el valor x"""
        return 1.0 / (1 + np.exp(-x))

    def derivada_sigmoide(self, x):
        """
        Calcula la derivada de la función sigmoide asumiendo que 'x'
        ya fue previamente pasado por la función 'sigmoide'
        """
        return x * (1 - x)

    def entrenar(self, X, y, epocas=1000, mostrarAvanceCada=100):
        """
        Realiza el entrenamiento hasta un número de épocas indicado
        """

        # Parte del truco del bias: Se inserta una columna de unos como última
        # entrada en la matriz de características, para tratar dicho parámetro
        # como uno de los valores a entrenar en la matriz de pesos.
        X = np.c_[X, np.ones((X.shape[0]))]

        for epoca in np.arange(0, epocas):
            # En cada época, se realiza el entrenamiento con cada punto de
            # datos.
            for (x, target) in zip(X, y):
                self.entrenamiento_parcial(x, target)

            # Muestra el avance según lo indicado por mostrarAvanceCada
            if epoca == 0 or (epoca + 1) % mostrarAvanceCada == 0:
                perdida = self.calcular_perdida(X, y)
                print("[INFO] epoca={}, perdida={:.7f}".format(
                    epoca + 1, perdida))

    def entrenamiento_parcial(self, x, y):
        # Construir la lista de activaciones de salida para cada capa mientras
        # los puntos de datos fluyen a través de la red; la primera activación
        # es un caso especial -- simplemente es el propio vector de
        # características.
        activaciones = [np.atleast_2d(x)]

        # Propagación hacia en frente FEEDFORWARD:
        for capa in np.arange(0, len(self.pesos)):
            # La activación de la capa actual se transmite hacia el frente
            # tomando el producto punto entre la activación de la capa anterior
            # y la matriz de pesos -- a esto se le llama "entrada de red" de la
            # capa actual
            red = activaciones[capa].dot(self.pesos[capa])

            # Se calcula la "salida de red" aplicando la función de activación
            # no lineal a la entrada de red
            salida = self.sigmoide(red)

            # once we have the red output, add it to our list of
            # activations
            activaciones.append(salida)

        # Propagación hacía atrás BACKPROPAGATION
        # Esta fase comienza calculando la diferencia entre nuestra *predicción*
        # (la activación final en nuestra lista) y el verdadero valor de verdad

        error = activaciones[-1] - y

        # A partir de aquí, necesitamos aplicar la regla de la cadena y
        # construir nuestra lista de deltas; la primera entrada en las deltas es
        # simplemente el error de la capa de salida multiplicada por la derivada
        # de nuestra función de activación para el valor de salida.
        deltas = [error * self.derivada_sigmoide(activaciones[-1])]

        # once you understand the chain rule it becomes super easy
        # to implement with a ‘for‘ loop -- simply loop over the
        # capas in reverse order (ignoring the last two since we
        # already have taken them into account)
        # Usando la regla de la cadena, recorremos las capas en orden inverso
        # (ignorando las últimas dos que ya fueron tomadas en cuenta)
        for capa in np.arange(len(activaciones) - 2, 0, -1):
            # La delta de la capa actual es el producto punto de la *capa
            # previa* con la matriz de pesos de la capa actual, seguida de la
            # multiplicación de la delta por la derivada de la función de
            # activación no lineal para la capa actual.
            delta = deltas[-1].dot(self.pesos[capa].T)
            delta *= self.derivada_sigmoide(activaciones[capa])
            deltas.append(delta)

        # Dado que generamos las deltas recorriendo las capas en orden inverso,
        # las invertimos
        deltas = deltas[::-1]

        # Fase de actualización de pesos
        for capa in np.arange(0, len(self.pesos)):
            # La actualización se hace tomando el producto punto de las
            # activaciones con sus deltas respectivas multiplicado por la taza
            # de aprendizaje. Todo esto se añade a la matriz de pesos
            # -- Este es el punto en que el aprendizaje ocurre
            self.pesos[capa] += -self.alpha * activaciones[capa].T.dot(deltas[capa])

    def predecir(self, X, aniadir_sesgo=True):
        """
        Inicializar las predicciones de salida como los vectores de entrada
        -- estos valores serán propagados (hacia adelante) a través de la red
        para obtener la predicción final.
        """
        prediccion = np.atleast_2d(X)

        if aniadir_sesgo:
            # Insertar una columna de unos como la última entrada en la matriz
            # de características (sesgo)
            prediccion = np.c_[prediccion, np.ones((prediccion.shape[0]))]

        for capa in np.arange(0, len(self.pesos)):
            # Calculo de la predicción de salida como el producto punto del
            # valor de activación actual 'prediccion' y la matriz de pesos
            # asociada con la capa actual. Ese valor luego es pasado por la
            # función de activación no lineal.
            prediccion = self.sigmoide(np.dot(prediccion, self.pesos[capa]))

        return prediccion

    def calcular_perdida(self, X, objetivos):
        """
        Calcula la diferencia entre predicción y valor objetivo
        """

        # Realizar predicciones para los puntos de entrada para calcular la
        # pérdida
        objetivos = np.atleast_2d(objetivos)
        predictions = self.predecir(X, aniadir_sesgo=False)
        perdida = 0.5 * np.sum((predictions - objetivos) ** 2)

        return perdida

    def guardar(self, archivo):
        """
        Guarda los datos de la red en el archivo dado para no perder el
        entrenamiento
        """
        with open(archivo, 'w') as f:
            print(f'{self.alpha}', file=f)
            for capa in self.capas:
                print(f'{capa}', file=f, end=' ')
            print(file=f)

            for matrix in self.pesos:
                w_aplanado = np.reshape(matrix,
                                        matrix.shape[0] * matrix.shape[1])

                for val in w_aplanado:
                    print(f'{val}', file=f, end=' ')

                print(file=f)

    @classmethod
    def cargar(cls, archivo):
        """
        Se cargan los pesos y demás valores de la red guardados mediante el
        método "guardar"
        """
        with open(archivo) as f:
            alpha = float(f.readline())
            capas = list(map(int, f.readline().split()))
            pesos = []
            for line in f:
                pesos = list(map(float, line.split()))
                pesos = np.array(pesos)
                pesos.append(pesos)

            red = cls(capas, alpha, pesos)

        return red
