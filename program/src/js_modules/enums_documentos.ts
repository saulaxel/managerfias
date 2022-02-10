
// Tipos disponibles
export const T_MONOGRAFIA = 0;
export const T_MAPA       = 1;
export const T_ESQUEMA    = 2;
export const T_CROMO      = 3;
export const T_BIOGRAFIA  = 4;

// Imágenes correspondientes a cada tipo. Su orden se tiene que corresponder con las constantes anteriores
interface NombreImagen {
    [key: number]: string
};

let IMAGEN_TIPO = <NombreImagen> {}

IMAGEN_TIPO[T_MONOGRAFIA] = "monografia.jpg";
IMAGEN_TIPO[T_MAPA]       = "mapa.jpg";
IMAGEN_TIPO[T_ESQUEMA]    = "esquema.jpg";
IMAGEN_TIPO[T_CROMO]      = "cromo.jpg";
IMAGEN_TIPO[T_BIOGRAFIA]  = "biografia.jpg";

export { IMAGEN_TIPO };
