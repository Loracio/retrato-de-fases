# ¿Qué es esto?
La idea de este repositorio es crear una librería que contenga distintas clases para pintar retratos de fases de distintos sistemas (2D, 3D, ...), para poder realizar los mismos de manera sencilla, puesto que no encontré ninguna opción que pareciera relativamente sencilla para realizarlos.

## Contribuir
El [código](#archivos) es abierto, todos podéis descargarlo y utilizarlo. Y también podéis contribuir si lo deseáis. Para ello, se puede hacer una de las siguientes opciones:
* Descargarse una rama del proyecto (fork), hacer una mejora y pedir su admisión a través de GitHub.
* Contactar por correo a **778841@unizar.es**

## Autores
- Víctor Loras Herrero
- Unai Lería Fortea

# Instalación
## Instalación con pip:
> $ pip install retratodefases

## Instalación con git:
Abrir una terminal en el directorio deseado:
> $ git clone https://github.com/Loracio/retrato-de-fases

## Instalación manual:
Visita la página de [retrato-de-fases](https://github.com/Loracio/retrato-de-fases) en github. Pulsar el botón verde con el texto *Codigo* y descargar en forma de zip.
Guardar y descomprimir el archivo en el directorio deseado.


# Ejemplos de uso
- ### [ejemplos.ipynb](examples/ejemplos.ipynb):
Ejemplos para ver cómo se utilizan las clases de RetratoDeFases2D.

- ### [ejemplosSliders.py](examples/ejemplosSliders.py) :
Contiene ejemplos de plots con sliders para retratos de fases 2D.

- ### [ejemploTrayectoria.py](examples/ejemploTrayectoria.py):
Contiene ejemplos de trayectorias 3D con y sin sliders.


# Instrucciones para utilizar la librería
Simplemente, deberemos importar la librería:
```python
import retratodefases
from retratodefases import *
```
Esto importará las clases que debe usar el usuario, por el momento son:
- [RetratoDeFases2D](.readme/retratodefases2d.md)
- [RetratoDeFases3D](.readme/retratodefases3d.md)
- [Trayectoria3D](.readme/trayectoria3d.md)

Todas ellas comparten un mismo tipo de primer argumento: una función que dadas unas coordenadas te devuelve la derivada de cada coordenada en ese punto.
# [Función dF](.readme/dFfuncion.md)
```python
def dF(x,y):
  return expresionX  ,  expresionY
```

También se pueden pasar variables extras en forma de diccionario. Por ejemplo para un oscilador armónico de frecuencia `w` (con valor estandar 1):
```python
def oscilador(x,y, *, w=1):
  return expresionX, expresionY
```


# [RetratoDeFases2D](.readme/retratodefases2d.md)
> *class* retratodefases.**RetratoDeFases2D**(*dF, RangoRepresentacion, \*, LongitudMalla=10, dF_args={}, Densidad=1, Polar=False, \*\*opciones*)

Permite representar un retrato de fases en dos dimensiones de una función [dF](.readme/dFfuncion.md) de 2 parámetros obligatorios.


# [RetratoDeFases3D](.readme(retratodefases3d.md))
> *class* retratodefases.**RetratoDeFases2D**(*dF, RangoRepresentacion, \*, LongitudMalla=10, dF_args={}, Densidad=1, Polar=False, \*\*opciones*)

Permite representar un retrato de fases en tres dimensiones de una función [dF](.readme/dFfuncion.md) de 3 parámetros obligatorios.

# [Trayectoria3D](.readme/trayectoria3d.md)
> *class* retratodefases.**Trayectoria3D**(*dF, \*, RangoRepresentacion=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, \*\*opciones*)

Permite representar trayectorias tridimensionales de una función [dF](.readme/dFfuncion.md) de 3 parámetros obligatorios.