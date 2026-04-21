# Proyecto-GeoEngine

Este es un proyecto personal que hice para practicar algebra lineal, simulacion y organizacion de codigo en Python.

La idea fue no quedarme solo con ejercicios sueltos o notebooks, sino llevar esos conceptos a algo mas concreto: un mini motor con vectores, matrices, transformaciones 3D, proyeccion y una simulacion simple de particulas con colisiones.

Mi objetivo con este proyecto fue trabajar fundamentos que me interesan para mi camino hacia ingenieria de IA: matematica aplicada, modelado, simulacion, estructura de software y visualizacion.

## Que hace

- Implementa vectores 3D y matrices 3x3 desde cero.
- Permite trabajar con rotaciones, escala, shear, determinante e inversa.
- Simula particulas con masa, gravedad, rebotes y colisiones por impulso.
- Incluye una interfaz visual en Tkinter para explorar transformaciones y fisica.
- Tiene tests para validar el nucleo matematico y fisico.

## Estructura

- `geoengine/algebra/`: vectores y matrices
- `geoengine/physics/`: particulas, mundo y colisiones
- `geoengine/rendering/`: proyeccion de puntos 3D
- `geoengine/app.py`: demo visual
- `geoengine/report.py`: modo headless para inspeccionar resultados
- `tests/`: pruebas automatizadas

## Como ejecutarlo

```powershell
.\.venv\Scripts\python.exe main.py
```

## Modo reporte

```powershell
.\.venv\Scripts\python.exe main.py --report
```

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Que quise mostrar con este proyecto

- Que puedo implementar conceptos matematicos sin depender completamente de librerias externas.
- Que puedo organizar un proyecto pequeno con una estructura clara y mantenible.
- Que me interesa entender lo que hay debajo de motores, simulaciones y herramientas visuales.
- Que puedo convertir teoria en algo interactivo y presentable.

## Cosas que me gustaria seguir agregando

- matrices 4x4 y camara libre
- quaternions
- una version web para que se pueda probar online
- export de animaciones o GIFs
- simulaciones mas complejas

## Nota personal

Todavia sigo estudiando y este proyecto forma parte de ese proceso. Lo hice con la idea de aprender en serio, no solo de llegar a un resultado visual. Si lo estas viendo como recruiter, para mi representa bastante bien como pienso: me gusta entender fundamentos, construir cosas desde abajo y despues llevarlas a algo usable.
