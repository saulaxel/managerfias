import os

def crear_directorio_si_no_existe(nombre: str):
    '''
    Intenta crear el directorio con el nombre indicado como parámetro
    Regresa True si el directorio fue creado y False si ya existía
    '''
    try:
        os.mkdir(nombre)
        return True
    except FileExistsError:
        return False


def separar_partes_nombre(archivo: str):
    '''
    Separa nombre y extensión del archivo en una lista, a la vez que elimina el resto de
    elementos de la ruta si esta está presente.
    Por ejemplo: separar_partes_nombre('/ruta/archivo.txt') -> ['archivo', 'txt']
    '''
    if type(archivo) != str:
        raise ValueError('El nombre de archivo debe ser una cadena')

    if archivo == '':
        raise ValueError('El nombre de archivo no debe estar vacío')

    return os.path.basename(archivo).split('.')

def extraer_nombre_base(archivo):
    '''
    Regresa el nombre del archivo sin extensión
    extraer_nombre_base('/ruta/archivo.txt') -> 'archivo'
    '''
    return separar_partes_nombre(archivo)[0]


def extraer_extension(archivo):
    '''
    Regresa la extensión de un archivo
    extraer_nombre_base('/ruta/archivo.txt') -> 'txt'
    '''
    partes = separar_partes_nombre(archivo)

    if len(partes) < 2:
        raise ValueError('El nombre de archivo no contiene extensión')

    return partes[-1]
