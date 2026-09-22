# Publicar el juego en el navegador (pygbag)

`pygbag` toma el proyecto Python y lo convierte en una pagina web usando
WebAssembly. No hace falta ningun servidor, backend ni Node.js: el resultado
son archivos estaticos.

## Probar en local

Desde la carpeta raiz del proyecto (`futbol-de-mesa/`):

```bash
python -m pygbag main.py
# abrir http://localhost:8000
```

## Generar el build

```bash
python -m pygbag --build main.py
```

Carpeta a publicar: **`build/web/`**

```
build/web/
├── index.html
├── futbol-de-mesa.apk
├── futbol-de-mesa.tar.gz
└── favicon.png
```

`build/web-cache/` es solo cache local de pygbag: no se publica (esta ignorada
en `.gitignore`).

Para ver exactamente lo que va a ver el visitante:

```bash
python -m http.server 8000 --directory build/web
```

## Publicacion automatica (recomendada)

El workflow `.github/workflows/deploy.yml` hace el build y el deploy en cada
push a `main`. Solo hay que activar **Settings > Pages > Source: GitHub Actions**.

## Publicacion manual con la rama `gh-pages`

Si se prefiere no usar Actions:

```bash
python -m pygbag --build main.py
touch build/web/.nojekyll
git checkout --orphan gh-pages
git rm -rf --cached .
cp -r build/web/* build/web/.nojekyll .
git add index.html favicon.png *.apk *.tar.gz .nojekyll
git commit -m "Publicar build web"
git push origin gh-pages
git checkout main
```

Despues: **Settings > Pages > Source: Deploy from a branch > `gh-pages` / `(root)`**.

## Otras opciones

itch.io: comprimir el contenido de `build/web/` en un `.zip` y subirlo como
proyecto HTML5 (marcando "This file will be played in the browser").

## Requisitos para que funcione en el navegador

- `main.py` en la raiz y con `asyncio.run(main())`.
- `await asyncio.sleep(0)` en cada vuelta del bucle (si no, el navegador se
  congela).
- Solo librerias disponibles en WebAssembly (por eso usamos unicamente
  `pygame-ce`).
- La pagina pide un click inicial ("Ready to start!") antes de arrancar: es el
  comportamiento normal de pygbag, porque el navegador necesita interaccion del
  usuario para habilitar el audio.
