# ¿Qué es esto?
La idea de este repositorio es crear una librería que contenga distintas clases para pintar retratos de fases de distintos sistemas (2D, 3D, ...), para poder realizar los mismos de manera sencilla, puesto que no encontré ninguna opción que pareciera relativamente sencilla para realizarlos.

## Contribuir
El [código](#archivos) es abierto, todos podéis descargarlo y utilizarlo. Y también podéis contribuir si lo deseáis. Para ello, se puede hacer una de las siguientes opciones:
* Descargarse una rama del proyecto (fork), hacer una mejora y pedir su admisión a través de GitHub.
* Contactar por correo a **778841@unizar.es**

## Autores
- Víctor Loras Herrero
- Unai Lería Fortea

## Archivos
- [retratodefases](retratodefases): Es el fichero que contiene todo lo necesario para usar la librería: clases, excepciones, funciones que se usan internamente...
- [ejemplos.ipynb](ejemplos.ipynb): Ejemplos para ver cómo se utilizan las clases del módulo [retratodefases](retratodefases)
- [README.md](README.md): Es lo que estás leyendo ahora mismo.
- [gitignore](.gitignore): sirve para decirle a Git qué archivos o directorios completos debe ignorar y no subir al repositorio de código. Como dice su nombre: ignóralo.

# Instrucciones para utilizar la librería
Simplemente, deberemos importar la librería escribiendo la ruta hasta ella. De momento, la librería contiene únicamente la clase RetratoDeFases2D, que sirve para realizar retratos de fases de sistemas bidimensionales. 

La idea de esta clase, es pasarle una función que devuelva las expresiones para las derivadas de dos parámetros (para que calcule los flujos en el espacio de fases). Será de la forma:

```python
def dF(x,y):
  return expresionX, expresionY
```
Donde también se pueden pasar variables extras en forma de diccionario. Por ejemplo para un oscilador armónico de frecuencia `w` (con valor estandar 1):
```python
def dF(x,y, *, w=1):
  return expresionX, expresionY
```
También deberemos indicar el rango de representación que queremos que se calcule. Esto puede indicarse de tres maneras:

1. Para representar sobre un dominio 'cuadrado', pasamos sólo el argumento `[limiteInferior , limiteSuperior]`. De esta manera los dos ejes tendrán el mismo rango.

2. Si queremos que tengan distinto rango, deberemos pasar el argumento de la siguiente manera:
`[[limiteInferiorEjeX, limiteSuperiorEjeX], [limiteInferiorEjeY, limiteSuperiorEjeY]]`

3. Si queremos representar desde 0 hasta cierto número, sólo hará falta poner ese número (también vale si es negativo). Obviamente, no podemos poner solo cero, pues sería un rango nulo.

Con estos dos argumentos, podemos inicializar un objeto de la clase `RetratoDeFases2D`. A continuación, se detallan los distintos argumentos opcionales:

* **Polar** : booleano con valor `False` por defecto. Se debe pasar como argumento a la función cuando los inputs de nuestra función `dF` se den en coordenadas polares.

* **Densidad** : controla la cercanía de las líneas de flujo en el espacio de fases. Su valor predefinido es 1. Aumentar mucho este valor aumenta considerablemente el tiempo de computación del retrato de fases.

* **LongitudMalla** : para calcular el retrato de fases, se crea una malla que depende del rango de representación dado, sobre la cual se calcula el campo de velocidades. El valor de esta variable es el número de puntos en la malla, multiplicado por la diferencia entre el rango inferior y el superior. El valor predefinido de esta variable es 10.

* **Titulo** : cadena de carácteres que aparece como título de la representación. Su valor predefinido es `'Retrato de Fases'`.

* **xlabel** : cadena de carácteres que aparece como título del eje X en la representación. Su valor predefinido es `'X'`.

* **ylabel** : cadena de carácteres que aparece como título del eje Y en la representación. Su valor predefinido es $\dot{X}$.


Una vez conocemos los argumentos de la clase, pasemos a los métodos de clase.

* **plot** : toma como argumentos los parámetros de la clase, es decir, no es necesario pasarle nada. Como argumento opcional toma el parámetro `color` que toma los valores de los mapas de colores indicados en [este enlace](https://matplotlib.org/stable/gallery/color/colormap_reference.html). 

* **add_slider** : añade un *slider* que permite cambiar el valor de una variable en tiempo de ejecucion del programa. Toma los siguientes argumentos:

**Obligatorios**:
* Cadena de texto con el nombre del parámetro a incluir en la barra desplazable, que debe coincidir con el nombre del parámetro en el diccionario de la función `dF`.

**Opcionales**:
* **valinit** : indica el valor inicial que toma la variable. Su valor predefinido es la mitad del valor de la variable.

* **valstep** : valor mínimo que varía la variable. Su valor predefinido es 0,1.

* **valinterval** : intervalo entre el que varía la variable. Su valor predefinido es `[-10, 10]`


De momento, estas son las funcionalidades que ofrece la librería. Pueden verse distintos ejemplos de uso en [ejemplos.ipynb](ejemplos.ipynb) y en [ejemplosSliders.py](ejemplosSliders.py)
 
 
