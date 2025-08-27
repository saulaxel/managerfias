# Historial de cambios del programa

## Versión 0.2.0 (Previo a la creación del repo de git)

- Campo de búsqueda
- Lista de sugerencias que muestra documentos que coinciden con el texto de
    búsqueda y lista de elecciones que guarda los elementos de interés para el
    dependiente
- Lista incompleta de documentos. Contiene casi todas las monografías, pero no
    todos los códigos están actualizados
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

## Version 0.2.2

- Se centra el icono del botón de recarga calculando apropiadamente el alto de
    línea
- Filtrando elementos por tipo

## Version 0.2.3

- Webpack agregado. Se hacen los arreglos apropiados a la exportación y al
    ámbito de las funciones afectadas
- Se añade Favicon y manifest para convertir la app en una PWA
- Corregir un bug que impedía añadir elementos diferentes a monografías

## Version 0.2.4
- Se separa el manejo de eventos y la actualización de la lista de sugerencias
- Se arregla la actualización tras elegir un filtro de documento distinto
- Se encuentra bug que impedía actualización cuando se borraba y volvía a
    escribir el mismo texto repetidas veces.
- Se encuentra bug que prevenía actualización cuando se borra el texto de
    búsqueda presionando el botón de ESCAPE.
- Reestructuración del index para que las monografías que elegiste aparezcan antes de las sugerencias.
- Corrección de algunos datos en la letra A de la base de datos

## version 0.2.5
- Se corrige actualización cuando se borra el texto de búsqueda mediante el
    tache provisto por chrome.
- Se coloca un borde en el input de búsqueda para facilitar su visualización

## Recolección de imágenes de las monografías

- Sin cambios razonables en el código de la aplicación
- Se escanearon todas las monografías por ambos lados y se extrajeron todas sus
    imágenes

## Cosas por hacer

- Arreglar la carga de múltiples imágenes para los mismos iconos
- Permitir cambiar entre listas para diferentes locales
- Habilidad para eliminar elementos individuales de la lista de elecciones
- Cuenta de usuarios
- Persistencia de los datos de acuerdo a la cuenta de usuario
- Eliminar letras obsoletas como LL y CH de los índices de documentos
- Añadir, editar y eliminar elementos de la lista digital directamente desde el
    sistema
- Modularización y pruebas de unidad
- En los resultados debe haber un aviso cuando la monografía comparte número
    con otra no relacionada
