# Sliders
> *class* retratodefases.sliders.**Slider**(*retrato, param_name, valinit=None, valstep=0.1, valinterval=[]*)

### **Esta clase no debe usarse por el usuario. Es controlada por el resto de objetos de manera automática.**

Permite modificar un parámetro opcional de una función [dF](dFfuncion.md) durante los plots para ver los cambios a tiempo real, o lo más parecido a tiempo real posible.

# add_slider
> *method* .**add_slider**(*param_name, \*, valinit=None, valstep=0.1, valinterval=10*)

Añade un slider que permite cambiar el valor de una variable en tiempo de ejecucion del programa. Toma los siguientes argumentos:

**Obligatorios**:
* Cadena de texto con el nombre del parámetro a incluir en la barra desplazable, que debe coincidir con el nombre del parámetro en el diccionario de la función `dF`.

**Opcionales**:
* **valinit** : indica el valor inicial que toma la variable. Su valor predefinido es la mitad del valor de la variable.

* **valstep** : valor mínimo que varía la variable. Su valor predefinido es 0,1.

* **valinterval** : intervalo entre el que varía la variable. Su valor predefinido es `[-10, 10]`