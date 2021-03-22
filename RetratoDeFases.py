from inspect import signature

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
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


        # Variables que el usuario no debe emplear: son para el tratamiento interno de la clase. Es por ello que llevan el prefijo "_"
        self._X, self._Y = np.meshgrid(np.linspace(self.Rango[0,0], self.Rango[0,1], self.L), np.linspace(self.Rango[1,0], self.Rango[1,1], self.L))   #Crea una malla de tamaño L²

        if self.Polar:   
            self._R, self._Theta = (self._X**2 + self._Y**2)**0.5, np.arctan2(self._Y, self._X) # Transformacion de coordenadas cartesianas a polares
            self._transformacionPolares()
        else:
            self._dX, self._dY = self.dF(self._X, self._Y, **self.dF_args) # Calcula el campo de velocidades en cada uno de los puntos de la malla


    def plot(self, *, color='rainbow', linewidth=1, parametro=None):
        
        if parametro:

            #TODO: comprobar que el parametro está en dF_args

            #TODO: pasar como argumento los limites de la barra y el salto entre cada valor (valstep)

            self._variable_plot(parametro, color=color)

        else:
            self._standard_plot(color, linewidth)

        

    def _standard_plot(self, color, linewidth):
        colores = (self._dX**2+self._dY**2)**(0.5)
        colores_norm = matplotlib.colors.Normalize(vmin=colores.min(), vmax=colores.max())

        plt.streamplot(self._X, self._Y, self._dX, self._dY, color=colores, cmap=color, norm=colores_norm, linewidth=1, density= self.Densidad)
        plt.axis('square')
        plt.axis([self.Rango[0,0], self.Rango[0,1], self.Rango[1,0], self.Rango[1,1],])
        
        plt.title(f'{self.Titulo}')
        plt.xlabel(f'{self.xlabel}')
        plt.ylabel(f'{self.ylabel}')
        plt.grid()
        plt.show()


    def _variable_plot(self, param_name, *, color='rainbow'):
        """
        Crea un plot variable en función del parámetro especificado `param_name`. 
        Debe ser el mismo nombre que en la definición de la función.
        """

        def update(val):
            ax.cla()
            self.dF_args.update({param_name:val})
            self.dibuja_streamplot(ax, color=color)
            fig.canvas.draw_idle()
        
        fig, ax = plt.subplots()
        stream = self.dibuja_streamplot(ax, color=color)
        fig.subplots_adjust(top=0.8)
        
        bbox = ax.get_position()
        axParametro = fig.add_axes([bbox.x0, bbox.y1+0.1, bbox.width, 0.03])
        sParametro = Slider(axParametro, param_name, -10.0, 10.0, valinit=self.dF_args[param_name], valstep=0.1)
        sParametro.on_changed(update)
        
        plt.show() 
    


    def _transformacionPolares(self):
        """
        Devuelve la expresión del campo de velocidades en cartesianas, si la expresión del sistema viene dada en polares
        """
        self._dR, self._dTheta = self.dF(self._R, self._Theta, *self.dF_args)
        self._dX, self._dY = self._dR*np.cos(self._Theta) - self._R*np.sin(self._Theta)*self._dTheta, self._dR*np.sin(self._Theta)+self._R*np.cos(self._Theta)*self._dTheta



    def dibuja_streamplot(self, ax, *, color='rainbow'):
        if self.Polar:
            self._transformacionPolares()
        else:
            self._dX, self._dY = self.dF(self._X, self._Y, **self.dF_args)
        colores = (self._dX**2+self._dY**2)**(0.5)
        colores_norm = matplotlib.colors.Normalize(vmin=colores.min(), vmax=colores.max())
        stream = ax.streamplot(self._X, self._Y, self._dX, self._dY, color=colores, cmap=color, norm=colores_norm, linewidth=1, density= self.Densidad)
        ax.set_xlim([self.Rango[0,0], self.Rango[0,1]])
        ax.set_ylim([self.Rango[1,0], self.Rango[1,1]])
        x0,x1 = ax.get_xlim()
        y0,y1 = ax.get_ylim()
        ax.set_aspect(abs(x1-x0)/abs(y1-y0))
        ax.set_title(f'{self.Titulo}')
        ax.set_xlabel(f'{self.xlabel}')
        ax.set_ylabel(f'{self.ylabel}')
        ax.grid()
        return stream


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

    @Rango.setter
    def Rango(self, value):
        def is_number(x):
            return isinstance(x, (float,int))
        def is_range(U):
            return isinstance(U, (list,tuple))

        if is_number(value):
            if value == 0:
                raise RangoInvalid('0 no es un rango válido')
            aux = [0,value]
            aux.sort()
            self._Rango = np.array([aux,aux])
            return

        if is_range(value):
            a,b = value
            if is_number(a) and is_number(b):
                self._Rango = np.array([[a,b]]*2)
                return

            if is_range(a) and is_range(b):
                try:
                    aa, ab = a
                    ba, bb = b
                    if is_number(aa) and is_number(ab) and is_number(ba) and is_number(bb):
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
