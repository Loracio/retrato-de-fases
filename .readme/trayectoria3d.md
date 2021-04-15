# Trayectoria3D
> *class* retratodefases.**Trayectoria3D**(*dF, \*, RangoRepresentacion=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, \*\*kargs*)

Clase que permite representar trayectorias dada una función [dF](../README.md) con 3 parámetros obligatorios.

| Atributos          | Métodos                                                                 |
| ------------------ | ----------------------------------------------------------------------- |
| dF                 | [posicion_inicial          ](#trayectoria3dposicion_inicial)            |
| dF_args            | [estbiliza                 ](#trayectoria3destabiliza)                  |
| Rango              | [add_slider                ](#trayectoria3dadd_slider)                  |
| values             | [plot                      ](#trayectoria3dplot)                        |
| velocity           | [compute_trayectory        ](#trayectoria3dcompute_trayectory)          |
| initial_conditions | [rungekutta_time_independet](#trayectoria3drungekutta_time_independent) |
| runge_kutta_step   |                                                                         |
| runge_kutta_freq   |                                                                         |
| n_points           |                                                                         |
| Titulo             |                                                                         |
| xlabel             |                                                                         |
| ylabel             |                                                                         |
| zlabel             |                                                                         |
| fig                |                                                                         |
| ax                 |                                                                         |
| sliders            |                                                                         |
| lines              |                                                                         |
| termalization      |                                                                         |
| color              |                                                                         |

### **Parametros**
* **dF** (función [dF](dFfuncion.md)) - función que devuelve las derivadas de cada coordenada.

* **dF_args** (dict) - diccionario con los valores que se quieran dar a la función **dF**.

* **RangoRepresentacion** (Opcional[list, float]) - mirar [definir rango en 3d](#definir-rangorepresentacion)

* **lines**=False (bool) - hace la representación con una línea contínua en vez de puntos.

* **color** (str) - si se pasa `'t'` colorea las trayectorias de puntos en función del tiempo. No funciona con lines=True. En cualquier otro caso usa el módulo de la velocidad.

* **termalization**=0 (int) - numero de puntos calculados de la trayectoria hasta que se empiezan a almacenar.

* **size**=0.5 (float) - tamaño e los puntos en la representación final.

* **numba**=False (bool) - compila la función [dF](dFfuncion.md) para acelerar la ejecución.

* **n_points** (int) - número de puntos totales que tendrán las figuras finales.

* **runge_kutta_spet** (float) - diferencial de tiempo del método runge-kutta de orden 4.

* **runge_kutta-freq** (int) - cantidad de puntos calculados entre posiciones guardadas.

* **Titulo** (str) -  cadena de carácteres que aparece como título de la representación. Su valor predefinido es `'Retrato de Fases'`.
  
* **xlabel** (str) -  cadena de carácteres que aparece como título del eje X en la representación. Su valor predefinido es `'X'`.
  
* **ylabel** (str) -  cadena de carácteres que aparece como título del eje Y en la representación. Su valor predefinido es `'Y'`.

* **zlabel** (str) -  cadena de carácteres que aparece como título del eje Z en la representación. Su valor predefinido es `'Z'`.

* **mark_start_point** (bool) - marka la posición inicial con un punto de mayor tamaño.


# Métodos
## *Trayectoria3D*.posicion_inicial
> *Trayectoria3D*.**posicion_inicial**(**posicion*)

El parámetro `posicion` debe ser una lista o un ndarray de 3 elementos.


## *Trayectoria3D*.estabiliza
> *Trayectoria3D*.**estabiliza**(**posicion*)
> 
El parámetro `posición` es opcional. En el caso de que no se introduzca, se tomará un número entre 0 y 1 para cada coordenada aleatoriamente.

## *Trayectoria3D*.add_slider
> *Trayectoria3D*.**add_slider**(*param_name, \*, valinit=None, valstep=0.1, valinterval=10*)
> 
Añade un [slider](slider.md) que permite cambiar el valor de una variable en tiempo de ejecucion del programa.


## *Trayectoria3D*.plot
> *Trayectoria3D*.**plot**

Toma como argumentos los parámetros de la clase, es decir, no es necesario pasarle nada. Como argumento opcional toma el parámetro `color` que toma los valores de los mapas de colores indicados en [este enlace](https://matplotlib.org/stable/gallery/color/colormap_reference.html). 


## *Trayectoria3D*.compute_trayectory
> *Trayectoria3D*.**compute_trayectory**(*initial_values*)

Dado una posición inicial en 3 coordenadas `initial_values` te devuelve una tupla con dos listas: posiciones y diferencias entre posiciones sucesivas. Devuelve `n_points` puntos.


## *Trayectoria3D*.rungekutta_time_independent
> *Trayectoria3D*.**rungekutta_time_independent**(*initial_values*)

Generador que dado una posición inicial  `initial_values`, devuelve el siguiente punto.

# Definir RangoRepresentacion:
1. Para representar sobre un dominio 'cubico' centrado en 0, pasamos sólo el argumento del medio lado `limiteLateral`. De esta manera los dos ejes tendrán el mismo rango.

2. Si queremos que tengan distinto rango, deberemos pasar el argumento de la siguiente manera:
`[[limiteInferiorEjeX, limiteSuperiorEjeX], [limiteInferiorEjeY, limiteSuperiorEjeY],  [limiteInferiorEjeZ, limiteSuperiorEjeZ]]`

3. Podemos mezcalr estas cosas. Por ejemplo un rango `[[0,20],[1,2],[-2,2]]` se puede definir como `[[0,20], [1,2], 2]`