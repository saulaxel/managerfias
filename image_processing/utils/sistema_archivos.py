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
    Separa nombre y extensión del archivo en una lista, a la vez que elimina el
    resto de elementos de la ruta si esta está presente.
    Por ejemplo: separar_partes_nombre('/ruta/archivo.txt') -> ['archivo', 'txt']
    '''
    if type(archivo) != str:
        raise ValueError('El nombre de archivo debe ser una cadena')

    if archivo == '':
        raise ValueError('El nombre de archivo no debe estar vacío')

    return os.path.basename(archivo).split('.')

def extraer_nombre_base(nombre_archivo):
    '''
    Regresa el nombre del archivo sin extensión dada una cadena con su ruta
    extraer_nombre_base('/ruta/archivo.txt') -> 'archivo'
    '''
    return separar_partes_nombre(archivo)[0]


def extraer_extension(nombre_archivo: str):
    '''
    Regresa la extensión de un archivo dada una cadena con su ruta
    extraer_nombre_base('/ruta/archivo.txt') -> 'txt'
    '''
    partes = separar_partes_nombre(nombre_archivo)

    if len(partes) < 2:
        raise ValueError('El nombre de archivo no contiene extensión')

    return partes[-1]


def guardar_bytes(nombre_archivo, bytes_a_guardar):
    '''
    Abre un archivo en modo de escritura binaria para guardar en los bytes
    pasados como parámetro
    '''
    with open(nombre_archivo, 'wb') as f:
        f.write(bytes_a_guardar)

