# Architecture Notes

GeoEngine fue reestructurado para que un recruiter o entrevistador pueda recorrerlo rapido:

- `algebra/` contiene el nucleo reusable.
- `physics/` encapsula la simulacion y evita mezclar reglas fisicas con la UI.
- `rendering/` concentra la proyeccion y deja abierta la puerta a cambiar de backend.
- `app.py` consume el motor, pero no define la matematica ni las colisiones.
- `report.py` permite demostrar comportamiento del motor sin depender de una ventana grafica.

Esta separacion hace que el proyecto sea pequeño, pero con una forma cercana a un engine real.
