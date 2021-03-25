# ¿Qué es esto?
La idea de este repositorio es crear un archivo que contenga distintas clases para pintar retratos de fases de distintos sistemas (2D, 3D, ...), y así poder importar el fichero que contenga las clases para poder emplearlo.

## Contribuir
El [código](#archivos) es abierto, todos podéis descargarlo y utilizarlo. Y también podéis contribuir si lo deseáis. Para ello, se puede hacer una de las siguientes opciones:
* Descargarse una rama del proyecto (fork), hacer una mejora y pedir su admisión a través de GitHub.
* Contactar por correo a **778841@unizar.es**

## Autores
- Víctor Loras Herrero
- Unai Lería Fortea

## Archivos
- [RetratoDeFases.py](RetratoDeFases.py): Archivo que contiene las distintas clases para pintar retratos de fase.
- [ejemplos.ipynb](ejemplos.ipynb): Ejemplos para ver cómo se utilizan las clases de [RetratoDeFases.py](RetratoDeFases.py)
- [README.md](README.md): Es lo que estás leyendo ahora mismo.
- [gitignore](.gitignore): sirve para decirle a Git qué archivos o directorios completos debe ignorar y no subir al repositorio de código. Como dice su nombre: ignóralo.

# Instrucciones sobre [RetratoDeFases.py](RetratoDeFases.py)
De momento contiene únicamente la clase RetratoDeFases2D, que sirve para realizar retratos de fases de sistemas bidimensionales. Contiene un inicializador y un método de clase ("función" de la clase para los no-familiarizados con Python) que realiza el plot con matplotlib.

La idea de esta clase, es pasarle una función que devuelva las expresiones para las derivadas de dos parámetros (para que calcule los flujos en el espacio de fases). Será de la forma:

```python
def dF(x,y):
  return expresionX, expresionY
```
También se pueden pasar variables extras en forma de diccionario. Por ejemplo para un oscilador armónico de frecuencia `w` (con valor estandar 1):
```python
def dF(x,y, *, w=1):
  return expresionX, expresionY
```
En este caso la llamada a la función debería incluir un diccionario con la variable `w` y su valor constante al kword `dF_args`:
```python
RetratoDeFases2D(dF, [-5, 5], dF_args={'w':3.14})
```
 
 # Instrucciones para usar [ejemplos.ipynb](ejemplos.ipynb)
 **Se debe tener en la misma carpeta el archivo [RetratoDeFases.py](RetratoDeFases.py) para que funcione**. Únicamente abir el notebook y ejecutar las celdas. En él se encuentra una explicación de cómo hacer uso de las clases de [RetratoDeFases.py](RetratoDeFases.py) correctamente.
 
 
