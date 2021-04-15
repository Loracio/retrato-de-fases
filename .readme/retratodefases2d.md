# RetratoDeFases2D
> *class* retratodefases.**RetratoDeFases2D**(*dF, RangoRepresentacion, \*, LongitudMalla=10, dF_args={}, Densidad=1, Polar=False, \*\*opciones*)
> 
Clase que permite representar retratos de fase dada una función [dF](../README.md) con 2 parámetros obligatorios.
| Atributos | Métodos                                   |
| --------- | ----------------------------------------- |
| dF        | [add_slider](#retratodefases2dadd_slider) |
| Rango     | [plot](#retratodefases2dplot)             |
| dF_args   |                                           |
| Densidad  |                                           |
| Polar     |                                           |
| L         |                                           |
| Titulo    |                                           |
| xlabel    |                                           |
| ylabel    |                                           |
| zlabel    |                                           |
| color     |                                           |
| sliders   |                                           |
| fig       |                                           |
| ax        |                                           |

### **Parametros**
* **dF** (función [dF](dFfuncion.md)) - función que devuelve las derivadas de cada coordenada.

* **dF_args** (dict) - diccionario con los valores que se quieran dar a la función **dF**.
  
* **RangoRepresentacion** (Opcional[list, float]) - mirar [definir rango en 2d](#definir-rangorepresentacion)
  
* **Polar** (bool) - booleano con valor `False` por defecto. Se debe pasar como argumento a la función cuando los inputs de nuestra función `dF` se den en coordenadas polares.
  
* **Densidad** (float) -  controla la cercanía de las líneas de flujo en el espacio de fases. Su valor predefinido es 1. Aumentar mucho este valor aumenta considerablemente el tiempo de computación del retrato de fases.

* **LongitudMalla** (int) -  para calcular el retrato de fases, se crea una malla que depende del rango de representación dado, sobre la cual se calcula el campo de velocidades. El valor de esta variable es el número de puntos en la malla, multiplicado por la diferencia entre el rango inferior y el superior. El valor predefinido de esta variable es 10.
  
* **Titulo** (str) -  cadena de carácteres que aparece como título de la representación. Su valor predefinido es `'Retrato de Fases'`.
  
* **xlabel** (str) -  cadena de carácteres que aparece como título del eje X en la representación. Su valor predefinido es `'X'`.
  
* **ylabel** (str) -  cadena de carácteres que aparece como título del eje Y en la representación. Su valor predefinido es $\dot{X}$.



# Métodos
## *RetratoDeFases2D*.plot
> *RetratoDeFases2D*.**plot**(*, color=None)

Toma como argumentos los parámetros de la clase, es decir, no es necesario pasarle nada. Como argumento opcional toma el parámetro `color` que toma los valores de los mapas de colores indicados en [este enlace](https://matplotlib.org/stable/gallery/color/colormap_reference.html). 



## *RetratoDeFases2D*.add_slider
> *RetratoDeFases2D*.**add_slider**(*param_name, \*, valinit=None, valstep=0.1, valinterval=10*)

Añade un [slider](slider.md) que permite cambiar el valor de una variable en tiempo de ejecucion del programa.

# Definir RangoRepresentacion:

1. Para representar sobre un dominio 'cuadrado', pasamos sólo el argumento `[limiteInferior , limiteSuperior]`. De esta manera los dos ejes tendrán el mismo rango.

2. Si queremos que tengan distinto rango, deberemos pasar el argumento de la siguiente manera:
`[[limiteInferiorEjeX, limiteSuperiorEjeX], [limiteInferiorEjeY, limiteSuperiorEjeY]]`

3. Si queremos representar desde 0 hasta cierto número, sólo hará falta poner ese número (también vale si es negativo). Obviamente, no podemos poner solo cero, pues sería un rango nulo.