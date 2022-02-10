import { IMAGEN_TIPO } from './js_modules/enums_documentos'
import { baseDatosGrafias } from './js_modules/datos_documentos_clip'

// Constantes
const FLECHA_ARRIBA    = 38;
const FLECHA_ABAJO     = 40;
const FLECHA_IZQUIERDA = 37;
const FLECHA_DERECHA   = 39;
const ENTER            = 13;
const ESCAPE           = 27;

// Funciones auxiliares
const normalizarTexto = function(texto: string) {
  texto = texto.normalize("NFD"); // Transforma un carácter de acento en una primitiva + código unicode de diacrílico
  texto = texto.replace(/[\u0300-\u036f]/g, ""); // La línea anterior permite quitar acentos con una simple sustitución
  texto = texto.toUpperCase(); // Javascript requiere usar regex para hacer comparaciones independientes
  // de mayúsculas y minúsculas, lo cual es más lento que la comparación normal.
  // En lugar de usar regex, se están transformando todas las cadenas a mayúsculas
  // para poder usar la comparación normal con la esperanza de que tenga mejor rendimiento.
  return texto;
};

const divSugerencias = document.getElementById("sugerencias");
const inputTexto = document.getElementById("texto") as HTMLInputElement;
const divElegidas = document.getElementById("elegidas");
if (divSugerencias == null || inputTexto == null || divElegidas == null ) {
    throw new Error("No se han encontrado los contenedores en el html");
}

let listaDivs: any[] = [];
let listaGrafias: any[] = [];

// Creando la lista de sugerencias por primera vez
(function() {
  for (let i = 0; i < baseDatosGrafias.length; i++) {
    let grafia = baseDatosGrafias[i];
    const divSugerencia = document.createElement("DIV");

    const divImagen = document.createElement("DIV");
    const imagen: HTMLImageElement = document.createElement("IMG") as HTMLImageElement;
    const src: string = "img/" + IMAGEN_TIPO[grafia.tipo];

    if (src === undefined) {
      throw Error("El tipo de ~grafia no tiene asignado una imagen");
    }
    imagen.src = src;
    divImagen.style.paddingRight = "10px";

    divImagen.appendChild(imagen);
    divSugerencia.appendChild(divImagen);

    const textoSugerencia = document.createTextNode(grafia.clave + " " + grafia.nombre);
    divSugerencia.appendChild(textoSugerencia);

    divSugerencia.classList.add("row");
    divSugerencia.classList.add("bg-info");
    divSugerencia.classList.add("rounded");
    divSugerencia.style.padding = "0.2em";
    divSugerencia.style.margin = "0.5em";
    divSugerencia.style.display = "none";
    divSugerencia.style.cursor = "pointer";
    divSugerencia.addEventListener('click', function() {
      seleccionarEnesimo(i);
    });

    divSugerencias.appendChild(divSugerencia);

    listaGrafias.push(normalizarTexto(grafia.nombre));
    listaDivs.push(divSugerencia);
  }
})();

// Variables que controlan las sugerencias
let previousText = "";
let listaSugerencias: any[] = [];
let indiceSeleccionado = 0;

const pintarComoSeleccionada = function(div: HTMLElement) {
  div.classList.remove("bg-info");
  div.classList.add("bg-primary");
};

const pintarComoNoSeleccionada = function(div: HTMLElement) {
  div.classList.remove("bg-primary");
  div.classList.add("bg-info");
}

const resetearSugerencias = function() {
  listaSugerencias = [];
  for (let i = 0; i < listaGrafias.length; i++) {
    listaDivs[i].style.display = "none";
    pintarComoNoSeleccionada(listaDivs[i]);
  }
}

const actualizarGrafias = function(evento?: Event) {
  const eventoTeclado: KeyboardEvent = evento as KeyboardEvent;
  const keyCode = eventoTeclado ? eventoTeclado.keyCode : 0;
  console.log(eventoTeclado);
  console.log(keyCode);

  // Teclas especiales
  if (keyCode === ENTER || keyCode === FLECHA_IZQUIERDA || keyCode === FLECHA_DERECHA) {
    aniadir();
    return;
  }

  if (keyCode == ESCAPE) {
    borrarTexto();
    return;
  }

  // No se modificó el texto, se presionaron las flechas del teclado
  if (keyCode == FLECHA_ARRIBA) {
    return;
  }

  if (keyCode == FLECHA_ABAJO) {
    return;
  }

  // Con el fin de evitar cálculos innecesarios
  const texto = normalizarTexto(inputTexto.value);

  if (texto === previousText) {
    return;
  }

  resetearSugerencias();

  if (texto === "") {
    // Esta condición va después de resetear sugerencias para que la cadena vacía no
    // muestre sugerencia alguna
    return;
  }

  // Calculamos y mostrando sugerencias
  const tokens = texto.split(" ");

  for (let i = 0; i < listaGrafias.length; i++) {

    let grafia = listaGrafias[i];

    let valida = true;
    for (let token of tokens) {
      if (!grafia.includes(token)) {
        valida = false;
        break;
      }
    }

    if (valida) {
      listaSugerencias.push(i);
      listaDivs[i].style.display = "flex";
    }

    pintarComoNoSeleccionada(listaDivs[i]);
  }

  // Se muestra el primer elemento seleccionado
  if (listaSugerencias.length > 0) {
    indiceSeleccionado = 0;
    let div = listaDivs[listaSugerencias[indiceSeleccionado]];
    pintarComoSeleccionada(div);
  }

  // Caché
  previousText = texto;
};
inputTexto.addEventListener('keyup', actualizarGrafias);

inputTexto.addEventListener('keydown', function(evento) {
  console.log(evento);
  if (evento.keyCode == FLECHA_ARRIBA) {
    evento.preventDefault();
    moverSeleccionArriba();
    return;
  }

  if (evento.keyCode == FLECHA_ABAJO) {
    evento.preventDefault();
    moverSeleccionAbajo();
    return;
  }
});

const borrarTexto = function() {
  previousText = "";
  inputTexto.value = "";
  actualizarGrafias();
};

const aniadir = function(indiceNodo?: number) {
  const indice = indiceNodo ?? 0;
  if (listaSugerencias.length > 0) {
    indiceNodo = listaSugerencias[indiceSeleccionado];
    const divEleccion = listaDivs[indice].cloneNode(true);

    pintarComoSeleccionada(divEleccion);

    divElegidas.appendChild(divEleccion);
  }

  previousText = normalizarTexto(inputTexto.value);
};

const resetearElegidas = function() {
  previousText = "";
  divElegidas.innerHTML = '';
};

const moverColorSeleccion = function(anterior: number, nuevo: number) {
  const indiceAnterior = listaSugerencias[anterior];
  const indiceNuevo = listaSugerencias[nuevo];

  pintarComoNoSeleccionada(listaDivs[indiceAnterior]);
  pintarComoSeleccionada(listaDivs[indiceNuevo]);
};

const moverSeleccionAbajo = function() {
  let anterior = indiceSeleccionado;
  indiceSeleccionado = (indiceSeleccionado + 1) % listaSugerencias.length;
  if (indiceSeleccionado >= listaSugerencias.length) {
    indiceSeleccionado = 0;
  }
  let nuevo = indiceSeleccionado;

  moverColorSeleccion(anterior, nuevo);
};

const moverSeleccionArriba = function() {
  let anterior = indiceSeleccionado;

  indiceSeleccionado--;
  if (indiceSeleccionado < 0) {
    indiceSeleccionado = listaSugerencias.length - 1;
  }
  let nuevo = indiceSeleccionado;

  moverColorSeleccion(anterior, nuevo);
};

const seleccionarEnesimo = function(n: Number) {
  let anterior = indiceSeleccionado;
  let encontrado = false;
  for (let i = 0; i < listaSugerencias.length; i++) {
    let indice = listaSugerencias[i];
    if (n == indice) {
      indiceSeleccionado = i;
      encontrado = true;
      break;
    }
  }

  if (!encontrado) {
    throw Error("Se está intentando seleccionar un objeto que no forma parte de la lista de sugerencias");
  }

  let nuevo = indiceSeleccionado;

  moverColorSeleccion(anterior, nuevo);
}

// Se ejecuta una vez la actualización
actualizarGrafias();

export { aniadir };
