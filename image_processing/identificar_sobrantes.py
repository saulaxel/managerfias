"""
Algunas monografías se escanearon dos veces o más debido a pequeños errores.
Este script tiene la finalidad de identificarlas.

Se va a usar una heurística sencilla para este fin:
  * Las imágenes con número par deberían ser del frente y las impares deben ser
    la parte de atrás de una monografía. Si una imagen no concuerda con lo
    esperado, es probable que se haya duplicado. Se mostrarán ambas versiones al
    usuario para que elija la correcta.
"""
import os
import os.path
import numpy as np
import shutil

from glob import glob
from argparse import ArgumentParser
from imutils import paths
from sklearn.model_selection import train_test_split
from enum import IntEnum
from typing import Tuple

from utils.sistema_archivos import extraer_nombre_base, extraer_extension
from utils import imagenes
from utils import log
from utils import Alternador

from clasificadores import ClasificadorPromedio

from pyimagesearch.datasets.cargador_simple_datos import CargadorSimpleDatos

# Funcionalidad central

class Eleccion(IntEnum):
    NINGUNA = 0
    ACTUAL = 1
    ANTERIOR = 2


FRENTE = 'front'  # Se usan un par de cadenas en lugar de una
REVERSO = 'back'  # enumeración porque así se pueden guardar de manera
                  # directa en un archivo

ARCHIVO_CLASIFICADOR_FRENTE_ATRAS = '03_promedios_frente_atras.txt'


# Auxiliares

def orden_numerico(nombre_archivo):
    '''
    Función para ordenar nombres de archivos en forma numérica
    Los archivos '2.txt', '11.txt',  '1.txt' '2_1.txt' generalmente se ordenarían como
    sigue:
        '1.txt', '11.txt', '2.txt'
    Pero si se interpreta la primera parte como un número entonces el orden debería ser:
        '1.txt', '2.txt', '11.txt'

    '''
    numero, resto = nombre_archivo.split('.', 1)
    return (int(numero), resto)


# Elecciones de elementos en la lista

def elegir_sobrante(elecciones_permitidas: Tuple[Eleccion]) -> Eleccion:
    '''
    Pide al usuario que elija de entre las opciones permitidas
    '''
    valor = -1
    try:
        valor = int(input('> '))
    except ValueError:
        pass # Elección no se pudo convertir a entero

    for eleccion in elecciones_permitidas:
        if (valor == int(eleccion)):
            return eleccion

    return Eleccion.NINGUNA


def obtener_eleccion(lista, eleccion, actual):
    '''
    Obtiene un elemento de la lista. Dicho elemento puede ser el indicado por la
    posición actual o un elemento aledaño de acuerdo con la el argumento
    'eleccion'
    '''
    if eleccion == Eleccion.ANTERIOR:
        return lista[actual - 1]
    elif eleccion == Eleccion.ACTUAL:
        return lista[actual]
    else:
        raise ValueError('Elección no válida')

def eliminar_eleccion(lista, eleccion, actual):
    '''
    Elimina un elemento de la lista. Dicho elemento puede ser el indicado por la
    posición actual o un elemento aledaño de acuerdo con la el argumento
    'eleccion'
    '''
    if eleccion == Eleccion.ANTERIOR:
        # Tenemos que retroceder el índice si se eliminó algo previo
        # para no saltarnos una imagen
        del lista[actual - 1]
    elif eleccion == Eleccion.ACTUAL:
        del lista[actual]
    else:
        raise ValueError('Elección no válida')


def elecciones_validas(indice_actual) -> Tuple[Eleccion]:
    '''
    Las elecciones válidas suelen ser la imagen actual y la anterior, excepto
    cuando actualmente nos encontramos en la primera imagen (no hay anterior)
    '''
    if indice_actual > 0:
        return (Eleccion.ACTUAL, Eleccion.ANTERIOR)

    return (Eleccion.ACTUAL,)


# Interfaz de usuario (tanto gráfica como no gráfica)

def mostrar_elecciones(lista, elecciones, actual):
    '''
    Muestra el elemento actual y los aledaños si es que existen. En la primera
    posición de la lista, por ejemplo, no existe un 'ANTERIOR'
    '''
    for i, eleccion in enumerate(elecciones):
        print(f'{i+1}) Eliminar {eleccion.name.lower()} -',
                obtener_eleccion(lista, eleccion, actual))

    print('Otra) No eliminar imagen')


def mostrar_varias_imagenes_hasta_tecla_presionada(imgs: Tuple):
    imagenes_pegadas = imagenes.pegar_horizontalmente(*imgs)
    imagenes_pegadas = imagenes.redimensionar_uniformemente(
                                    imagenes_pegadas,
                                    razon=0.3)

    imagenes.mostrar_hasta_tecla_presionada('Imagenes', imagenes_pegadas)

# Funcionalidad

def filtrar_sobrantes(rutas_imagenes, cp: ClasificadorPromedio):
    rutas_filtradas = rutas_imagenes.copy()
    clasificacion_esperada = Alternador(FRENTE, REVERSO)
    # La lista de rutas va a ser modificada en el propio ciclo, por lo que no
    # se puede recorrer mediante un for
    actual = 0
    while actual < (largo := len(rutas_filtradas)):
        # Obtener la clasificación de la imagen
        imagen_actual = imagenes.cargar(rutas_filtradas[actual])
        vector = imagenes.aplanar_una(imagen_actual)

        clasificacion = cp.predecir(vector)[0]

        if clasificacion != clasificacion_esperada.valor_actual():
            # Debería haber una imagen de frente seguida de una del reverso,
            # pero entrar a este if significa que no es el caso y se preguntará
            # al usuario si quiere eliminar alguna.
            # Se da la opción de dejar la lista como está, ya que la predicción
            # no es infalible, y puede significar que no hay realmente una
            # imagen sobrante a eliminar

            elecciones = elecciones_validas(actual)
            imagenes_a_mostrar = [imagen_actual]

            if Eleccion.ANTERIOR in elecciones:
                imagenes_a_mostrar.append(imagenes.cargar(rutas_filtradas[actual - 1]))

            mostrar_varias_imagenes_hasta_tecla_presionada(imagenes_a_mostrar)
            mostrar_elecciones(rutas_filtradas, elecciones, actual)
            sobrante = elegir_sobrante(elecciones)

            if sobrante != Eleccion.NINGUNA:
                eliminar_eleccion(rutas_filtradas, sobrante, actual)
                actual -= 1
                clasificacion_esperada.cambiar_valor()

        clasificacion_esperada.cambiar_valor()
        actual += 1

    if len(rutas_filtradas) % 2 != 0:
        log.msg('Número impar encontrado, eliminando el último lugar', nivel=log.DEBUG)
        log.msg(rutas_filtradas[-1], nivel=log.DEBUG)
        del rutas_filtradas[-1]

    return rutas_filtradas


def eliminar_sobrantes_en_carpetas(cp: ClasificadorPromedio,
                                   ruta_entrada: str,
                                   ruta_salida: str):
    contador_imagen = 0
    for raiz, directorios, archivos in os.walk(ruta_entrada):
        # Solo se toman en cuenta carpetas sin subdirectorios (el fondo
        # de la estructura de carpetas) para no tomar en cuenta la ruta
        # carpeta principal
        if not directorios:

            # Los archivos están numerados 0.jpeg, 1.pjeg, 2.jpeg...,
            # y así sucesivamente. El orden lexicográfico es tiene relevancia
            archivos.sort(key=orden_numerico)
            rutas_completas = [f'{raiz}/{nombre_imagen}' for nombre_imagen in archivos]

            base = extraer_nombre_base(raiz)

            lista_filtrada = list(filtrar_sobrantes(rutas_completas, cp))

            for nombre_imagen in lista_filtrada:
                ruta_actual = nombre_imagen
                extension = extraer_extension(ruta_actual)
                nueva_ruta = f'{ruta_salida}/{contador_imagen}.{extension}'
                shutil.copy(ruta_actual, nueva_ruta)
                contador_imagen += 1



# Programa principal
def main():
    ap = ArgumentParser()
    ap.add_argument('-e', '--ruta-entrada',
            default='../scanned_images/img_cropped/')
    ap.add_argument('-s', '--ruta-salida',
            default='../scanned_images/img_no_repeated')
    args = vars(ap.parse_args())

    cp = ClasificadorPromedio.cargar(ARCHIVO_CLASIFICADOR_FRENTE_ATRAS)

    ruta_entrada = args['ruta_entrada']
    ruta_salida = args['ruta_salida']

    eliminar_sobrantes_en_carpetas(cp, ruta_entrada, ruta_salida)


if __name__ == '__main__':
    main()
