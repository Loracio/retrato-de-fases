# Función dF
Función que debe devolver las derivadas de las coordenadas:
```python
def dF(x,y):
  return expresionX  ,  expresionY
```
Debe tener tantos parámetros obligatorios como elementos devuelva.

## Parámetros opcionales
Se pueden utilizar parámetros opcionales. Estos pueden ser variados con [sliders](slider.md) en el resto de clases del módulo. Un ejemplo de definición para un oscilador en dos dimensiones podría ser:
```python
def oscilador(x,y, *, w=1):
  return expresionX, expresionY
```
Donde `expresionX` y `expresionY` serán funciones de `x`, `y` y `w`.

## Definición general
De manera general se definiría de la siguiente manera:
```python
def dF(*args, *, **kargs) -> tuple:
```
Donde se cumpla:
```python
len(dF(*args, **kargs)) == len(args)
```