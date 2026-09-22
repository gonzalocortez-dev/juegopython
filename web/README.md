# Publicar el juego en el navegador (pygbag)

`pygbag` toma el proyecto Python y lo convierte en una pagina web usando
WebAssembly. No hace falta ningun servidor ni Node.js.

## 1. Probar en local

Desde la carpeta raiz del proyecto (`futbol-de-mesa/`):

```bash
pygbag .
```

Despues abrir en el navegador:

```
http://localhost:8000
```

La primera carga tarda unos segundos porque el navegador descarga Python.

## 2. Generar la version publicable

```bash
pygbag --build .
```

Queda todo en la carpeta `build/web/`:

```
build/web/
├── index.html
├── futbol-de-mesa.apk   (el juego empaquetado)
└── favicon.png
```

## 3. Subirlo a internet

Cualquier hosting de archivos estaticos sirve. Ejemplo con GitHub Pages:

1. Subir el contenido de `build/web/` a una rama `gh-pages`.
2. Activar Pages en Settings > Pages apuntando a esa rama.

Tambien funciona en itch.io: comprimir `build/web/` en un `.zip` y subirlo
como proyecto HTML5.

## Detalles importantes para que funcione en el navegador

- `main.py` tiene que estar en la raiz y usar `asyncio.run(main())`.
- El bucle principal tiene que hacer `await asyncio.sleep(0)` en cada frame,
  si no el navegador se congela.
- No se pueden usar librerias que no existan en WebAssembly (por eso solo
  usamos `pygame-ce`).
