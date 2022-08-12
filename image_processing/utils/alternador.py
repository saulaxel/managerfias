
class Alternador:
    def __init__(self, valor1, valor2):
        self.__estado = 0
        self.__valor1 = valor1
        self.__valor2 = valor2

    def cambiar_valor(self):
        self.__estado = 1 - self.__estado

    def valor_actual(self):
        return self.__valor2 if self.__estado else self.__valor1
