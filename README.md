# GeoEngine

GeoEngine es un sandbox interactivo de algebra lineal y fisica de particulas construido en Python. La idea no es solo "mostrar una ventana", sino demostrar criterio de ingenieria: un nucleo matematico testeado, una separacion clara por modulos y una demo visual que comunica intuicion tecnica rapido.

## Por que este proyecto sirve para portfolio

- Convierte conceptos de algebra lineal en una experiencia visual e interactiva.
- Muestra modelado orientado a objetos, diseno modular y validacion automatizada.
- Une matematica, simulacion y presentacion de producto en un repo chico pero serio.
- Tiene un modo visual para demo y un modo headless para inspeccion automatizada.

## Que incluye

- `geoengine/algebra/`: vectores 3D y matrices 3x3 con operaciones geometricas y algebraicas.
- `geoengine/physics/`: particulas con masa, impulsos, gravedad y colisiones.
- `geoengine/rendering/`: proyeccion de puntos 3D a pantalla.
- `geoengine/app.py`: dashboard Tkinter con escenas de transformaciones y fisica.
- `geoengine/report.py`: resumen headless para validacion rapida o CI.

## Demo local

```powershell
.\.venv\Scripts\python.exe main.py
```

## Reporte headless

```powershell
.\.venv\Scripts\python.exe main.py --report
```

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Arquitectura

```text
geoengine/
  algebra/
  physics/
  rendering/
  app.py
  cli.py
  report.py
  scenes.py
tests/
main.py
```

## Temas tecnicos para contar en una entrevista

- Como modelar rotaciones, escala y shear con matrices 3x3.
- Como resolver colisiones de particulas usando impulso y conservacion aproximada de momento.
- Como desacoplar el nucleo matematico del render y de la UI.
- Como disenar una demo que funcione tanto en modo visual como en modo headless.

## Proximos upgrades fuertes

- Matrices 4x4 y camara libre
- quaternions para orientacion
- export de frames o GIFs
- escenas con sistemas de particulas mas grandes
- integradores numericos mas avanzados
