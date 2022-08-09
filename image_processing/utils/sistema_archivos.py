import os

def crear_directorio_si_no_existe(nombre):
    try:
        os.mkdir(nombre)
    except FileExistsError:
        print('Directorio ya existe')


def extraer_nombre_base(archivo):
    return os.path.basename(archivo).split('.')[0]


def extraer_extension(archivo):
    return os.path.basename(archivo).split('.')[1]
