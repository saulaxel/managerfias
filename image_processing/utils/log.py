import logging
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL

NIVEL_COMO_CADENA = {
    NOTSET: "-",
    DEBUG: "DEBUG",
    INFO: "INFO",
    WARNING: "ADVERTENCIA",
    ERROR: "ERROR",
    CRITICAL: "CRÍTICO"
}
nivel_requerido = INFO

METODO_LOGGING = {
    DEBUG: logging.debug,
    INFO: logging.info,
    WARNING: logging.warning,
    ERROR: logging.error,
    CRITICAL: logging.critical
}

# Crear y configurar un archivo como bitácora de los mensajes
def configurar_logger(nuevo_nivel_requerido):
    '''
    Configura el archivo al que replicar los mensajes y establece el nivel que
    requieren los mensajes actualmente para mostrarse y enviarse a dicho archivo
    '''
    global nivel_requerido
    global logger

    logging.basicConfig(filename='log.txt', level=nuevo_nivel_requerido)

    # El estado actual se guarda en variables globales
    logger = logging.getLogger()
    nivel_requerido = nuevo_nivel_requerido

def msg(*msg, sep=' ', end='\n', nivel=INFO):
    '''
    Imprime un mensaje si tiene el nivel (severidad) apropiado o superior y
    también lo envía al archivo previamente configurado
    '''

    if nivel >= nivel_requerido:
        prefijo = f'[{NIVEL_COMO_CADENA[nivel]}]'
        metodo_logging = METODO_LOGGING[nivel]

        print(f'[{NIVEL_COMO_CADENA[nivel_requerido]}]', *msg, sep=sep, end=end)
        metodo_logging(sep.join(msg) + end)

configurar_logger(DEBUG)
