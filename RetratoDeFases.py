from inspect import signature

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox
import numpy as np


class RetratoExceptions(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class dFNotCallable(RetratoExceptions):
    def __init__(self, func):
        super().__init__(f"El objeto {func} no es una función")

class dFInvalid(RetratoExceptions):
    def __init__(self, sig, dF_args):
        super().__init__(f"La funcion `dF` tiene {len(sig.parameters)} argumentos, se han pasado {2+len(dF_args)}")

class dF_argsInvalid(RetratoExceptions):
    def __init__(self, dF_args):
        super().__init__(f"El objeto `dF_args={dF_args}` debe ser un diccionario, no {type(dF_args)}")

class RangoInvalid(RetratoExceptions):
    def __init__(self, text):
        super().__init__(f"El rango no es válido: {text}")


class _updateSlider():
    def __init__(self, retrato, param_name, color):
        self.retrato = retrato
        self.param_name = param_name
        self.color = color
    
    def __call__(self, value, *, color=None):
        self.retrato.ax.cla()
        self.retrato._sliders[self.param_name]['value'] = value
        self.retrato.dibuja_streamplot(color=self.color)
        self.retrato.fig.canvas.draw_idle()


class RetratoDeFases2D:
    """
    Hace un retrato de fases de un sistema 2D.
    """
    def __init__(self, dF, RangoRepresentacion, *, LongitudMalla=10, dF_args={}, Densidad = 1, Polar = False, Titulo = 'Retrato de Fases', xlabel = 'X', ylabel = r"$\dot{X}$"):
        """
        Inicializador de clase: inicializa las variables de la clase a los valores pasados. 
        También se definen las variables que se emplean internamente en la clase para realizar el diagrama.
        Se le debe pasar obligatoriamente una función que contenga la expresión de las derivadas de los parámetros.
        """

        # Variables obligatorias
        self.dF_args = dF_args                           # Argumentos extras que haya que proporcionar a la función dF
        self.dF = dF                                     # Derivadas de las variables respecto al tiempo
        self.Rango = RangoRepresentacion                 # Rango de representación del diagrama
        
        # Variables no obligatorias
        self.L = int (LongitudMalla*abs(self.Rango[0,0]-self.Rango[0,1]))                     # Número de puntos por eje para representar el diagrama (habrá L² puntos)
        self.Densidad = Densidad                                                              # Controla la cercanía de las líneas de flujo
        self.Polar = Polar                                                                    # Si se pasan las coordenadas en polares, marcar como True.
        self.Titulo = Titulo                                                                  # Titulo para el retrato de fases.
        self.xlabel = xlabel                                                                  # Titulo en eje X
        self.ylabel = ylabel                                                                  # Titulo en eje Y


        # Variables para la representación
        self.fig, self.ax = plt.subplots()
        self._sliders = {}

        # Variables que el usuario no debe emplear: son para el tratamiento interno de la clase. Es por ello que llevan el prefijo "_"
        self._X, self._Y = np.meshgrid(np.linspace(self.Rango[0,0], self.Rango[0,1], self.L), np.linspace(self.Rango[1,0], self.Rango[1,1], self.L))   #Crea una malla de tamaño L²

        if self.Polar:   
            self._R, self._Theta = (self._X**2 + self._Y**2)**0.5, np.arctan2(self._Y, self._X) # Transformacion de coordenadas cartesianas a polares


    def plot(self, *, color='rainbow'):
        self.dibuja_streamplot(color=color)


    def dibuja_streamplot(self, *, color='rainbow'):
        self.dF_args = {name: value['value'] for name, value in self._sliders.items() if value['value']!= None}
        if self.Polar:
            self._transformacionPolares()
        else:
            self._dX, self._dY = self.dF(self._X, self._Y, **self.dF_args)
        colores = (self._dX**2+self._dY**2)**(0.5)
        colores_norm = matplotlib.colors.Normalize(vmin=colores.min(), vmax=colores.max())
        stream = self.ax.streamplot(self._X, self._Y, self._dX, self._dY, color=colores, cmap=color, norm=colores_norm, linewidth=1, density= self.Densidad)
        self.ax.set_xlim([self.Rango[0,0], self.Rango[0,1]])
        self.ax.set_ylim([self.Rango[1,0], self.Rango[1,1]])
        x0,x1 = self.ax.get_xlim()
        y0,y1 = self.ax.get_ylim()
        self.ax.set_aspect(abs(x1-x0)/abs(y1-y0))
        self.ax.set_title(f'{self.Titulo}')
        self.ax.set_xlabel(f'{self.xlabel}')
        self.ax.set_ylabel(f'{self.ylabel}')
        self.ax.grid()
        
        return stream


    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10, color='rainbow'):
        """
        Añade un slider sobre un plot ya existente.
        """

        self.fig.subplots_adjust(bottom=0.25)

        if self._is_number(valinterval):
            if valinterval == 0:
                raise RangoInvalid('0 no es un rango válido')
            valinterval = [-valinterval,valinterval]

        elif self._is_range(valinterval):
            a,b = valinterval
            if self._is_number(a) and self._is_number(b):
                valinterval = [a,b]
            else:
                raise RangoInvalid('el rango (1D) debe ser o un real o una lista de dos')
        else:
            raise RangoInvalid(f'{valinterval} no es un rango válido')
        valinterval.sort()
        
        sbox = self.ax.get_position()
        ax_Parametro = self.fig.add_axes([0.25, 0.015 + 0.05*len(self._sliders), 0.5, 0.03])
        aux = {'valinit':valinit} if valinit else {}

        self._sliders.update({param_name:{
            'value':valinit,
            'sxbox': sbox,
            'axParametro': ax_Parametro,
            'sParametro': Slider(ax_Parametro, param_name, valinterval[0], valinterval[1], valstep=valstep, **aux)
        }})
        self._sliders[param_name]['sParametro'].on_changed(_updateSlider(self, param_name, color))
    
    
    def _transformacionPolares(self):
        """
        Devuelve la expresión del campo de velocidades en cartesianas, si la expresión del sistema viene dada en polares
        """
        self._dR, self._dTheta = self.dF(self._R, self._Theta, **self.dF_args)
        self._dX, self._dY = self._dR*np.cos(self._Theta) - self._R*np.sin(self._Theta)*self._dTheta, self._dR*np.sin(self._Theta)+self._R*np.cos(self._Theta)*self._dTheta



    # Funciones para asegurarse que los parametros introducidos son válidos
    @property
    def dF(self):
        return self._dF

    @dF.setter
    def dF(self, func):
        if not callable(func):
            raise dFNotCallable(func)
        sig = signature(func)
        if len(sig.parameters)<2 + len(self.dF_args):
            raise dFInvalid(sig, self.dF_args)
        self._dF = func

    @property
    def Rango(self):
        return self._Rango

    @staticmethod
    def _is_number(x):
        return isinstance(x, (float,int))
    @staticmethod
    def _is_range(U):
        return isinstance(U, (list,tuple))

    @Rango.setter
    def Rango(self, value):
        def _is_number(x):
            return isinstance(x, (float,int))
        def _is_range(U):
            return isinstance(U, (list,tuple))

        if _is_number(value):
            if value == 0:
                raise RangoInvalid('0 no es un rango válido')
            aux = [0,value]
            aux.sort()
            self._Rango = np.array([aux,aux])
            return

        if _is_range(value):
            a,b = value
            if _is_number(a) and _is_number(b):
                self._Rango = np.array([[a,b]]*2)
                return

            if _is_range(a) and _is_range(b):
                try:
                    aa, ab = a
                    ba, bb = b
                    if _is_number(aa) and _is_number(ab) and _is_number(ba) and _is_number(bb):
                        self._Rango = np.array([[aa,ab],[ba, bb]])
                except Exception:
                    raise RangoInvalid('Error al convertir a rango tipo: [ [], [] ].')
        else:
            raise RangoInvalid(f"{value} no es un rango coherente")
    

    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise dF_argsInvalid(value)
        self._dF_args = value