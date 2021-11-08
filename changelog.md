# Historial de cambios del programa

## Versión 0.2.0 (Previo a la creación del repo de git)

- Campo de búsqueda
- Lista de sugerencias que muestra documentos que coinciden con el texto de
    búsqueda y lista de elecciones que guarda los elementos de interés para el
    dependiente
- Botones para añadir y reiniciar la lista de elecciones
- La búsqueda responde de forma inmediata al escribir
- Búsqueda independiente de mayúsculas y minúsculas, de acentos y eñes, y
    también de otros símbolos compuestos mediante normalización Unicode
- Función para borrado rápido del campo de búsqueda

## Versión 0.2.1

- Corrección de bug en que se mostraban los resultados de la búsqueda antes de
    insertar la última letra en el campo de texto mediante cambio de evento
    keydown a input en los manejadores del campo de texto
- Se añaden las palabras "Sugerencias" y "Elegidas" encima de las listas
- Se coloca un borde alrededor de las listas del punto anterior