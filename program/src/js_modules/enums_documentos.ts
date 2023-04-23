
// Tipos disponibles
export const T_ALL        = -1;
export const T_MONOGRAFIA = 0;
export const T_MAPA       = 1;
export const T_ESQUEMA    = 2;
export const T_CROMO      = 3;
export const T_BIOGRAFIA  = 4;

// Imágenes correspondientes a cada tipo. Su orden se tiene que corresponder con las constantes anteriores
interface NombreImagen {
    [key: number]: string
};

let SRC_TIPO_IMAGEN = <NombreImagen> {}

SRC_TIPO_IMAGEN[T_MONOGRAFIA] = "monografia.jpg";
SRC_TIPO_IMAGEN[T_MAPA]       = "mapa.jpg";
SRC_TIPO_IMAGEN[T_ESQUEMA]    = "esquema.jpg";
SRC_TIPO_IMAGEN[T_CROMO]      = "cromo.jpg";
SRC_TIPO_IMAGEN[T_BIOGRAFIA]  = "biografia.jpg";


let tipo_doc_a_str = function(tipo: number) {
    if (tipo == T_ALL) {
        return 'todos';
    }
    else if (tipo == T_MAPA) {
        return 'mapa';
    }
    else if (tipo == T_CROMO) {
        return 'cromo';
    }
    else if (tipo == T_ESQUEMA) {
        return 'esquema';
    }
    else if (tipo == T_BIOGRAFIA) {
        return 'biografia';
    }
    else if (tipo == T_MONOGRAFIA) {
        return 'monografia';
    }

    throw new Error('Tipo desconocido');
}

let str_a_tipo_doc = function(str_tipo: string) {
    if (str_tipo === 'todos') {
        return T_ALL;
    }
    else if (str_tipo === 'mapas') {
        return T_MAPA;
    }
    else if (str_tipo === 'cromos') {
        return T_CROMO;
    }
    else if (str_tipo === 'esquemas') {
        return T_ESQUEMA;
    }
    else if (str_tipo === 'biografias') {
        return T_BIOGRAFIA;
    }
    else if (str_tipo === 'monografias') {
        return T_MONOGRAFIA;
    }

    throw new Error(`Tipo desconocido ${str_tipo}`);
}

export { SRC_TIPO_IMAGEN, tipo_doc_a_str, str_a_tipo_doc };
