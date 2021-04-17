from inspect import signature

from .exceptions import *
from . import sliders
from .utils import utils

import matplotlib
import matplotlib.pyplot as plt

import numpy as np

class RetratoDeFases3D:
    """
    Hace un retrato de fases de un sistema 3D.
    """
    _name_ = 'RetratoDeFases3D'
    def __init__(self, dF, RangoRepresentacion, *, LongitudMalla=10, dF_args={}, Polar = False, Titulo = 'Retrato de Fases', xlabel = 'X', ylabel = 'Y', zlabel = 'Z', color='rainbow'):
        """
        Inicializador de clase: inicializa las variables de la clase a los valores pasados. 
        También se definen las variables que se emplean internamente en la clase para realizar el diagrama.
        Se le debe pasar obligatoriamente una función que contenga la expresión de las derivadas de los parámetros.
        """

        # Variables obligatorias
        self.dF_args = dF_args                           # Argumentos extras que haya que proporcionar a la función dF
        self.dF = dF                                     # Derivadas de las variables respecto al tiempo
        self.Rango = RangoRepresentacion                 # Rango de representación del diagrama
        self.dimension = 3                               # Dimensión en la que estamos trabajando
        
        # Variables no obligatorias
        self.L = LongitudMalla                                                                # Número de puntos por eje para representar el diagrama (habrá L² puntos)
        self.Polar = Polar                                                                    # Si se pasan las coordenadas en polares, marcar como True.
        self.Titulo = Titulo                                                                  # Titulo para el retrato de fases.
        self.xlabel = xlabel                                                                  # Titulo en eje X
        self.ylabel = ylabel                                                                  # Titulo en eje Y
        self.zlabel = zlabel                                                                  # Titulo en eje Z


        # Variables para la representación
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.color = color
        self.sliders = {}

        # Variables que el usuario no debe emplear: son para el tratamiento interno de la clase. Es por ello que llevan el prefijo "_"
        self._XYZ = np.meshgrid(*[np.linspace(*r, l) for r, l in zip(self.Rango, self.L)])
        self._dXYZ = []*3

        #* Teóricamente, debería estar arreglado, pero repito, teóricamente. Bueno, es incorrecto por lo que explico en los comentarios de las líneas anteriores, pero sería meterle las componentes de la lista
        if self.Polar:   
            self._R, self._Theta, self._Phi = (self._XYZ[0]**2 + self._XYZ[1]**2 + self._XYZ[2]**2)**0.5, np.arctan2(self._XYZ[1], self._XYZ[0]), np.arctan2(((self._XYZ[0]**2 + self._XYZ[1]**2)**0.5), self._XYZ[2])  # Transformacion de coordenadas cartesianas a esféricas


    def plot(self, *, color=None):
        self._dibuja_streamplot(color=color if color else self.color)


    def norma(self):
        cuadrado = lambda x: x*x
        result = np.zeros(self.L)
        for i in self._XYZ:
            result += i**2
        return result**0.5


    def _dibuja_streamplot(self, *, color=None):

        self.dF_args = {name: slider.value for name, slider in self.sliders.items() if slider.value!= None}

        if self.Polar:
            self._transformacionEsfericas()
        else:
            self._dXYZ = self.dF(*self._XYZ, **self.dF_args)
        stream = self.ax.quiver(*self._XYZ, *self._dXYZ, length=0.01)
        self.ax.set_title(f'{self.Titulo}')
        self.ax.set_xlabel(f'{self.xlabel}')
        self.ax.set_ylabel(f'{self.ylabel}')
        self.ax.set_zlabel(f'{self.zlabel}')
        self.ax.grid()
        
        return stream


    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Añade un slider sobre un plot ya existente.
        """
        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.fig.subplots_adjust(bottom=0.25)

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])
    
    
    def _transformacionEsfericas(self):
        """
        Devuelve la expresión del campo de velocidades en cartesianas, si la expresión del sistema viene dada en esféricas
        """
        self._dR, self._dTheta, self._dPhi = self.dF(self._R, self._Theta, self._Phi **self.dF_args)
        self._dXYZ[0], self._dXYZ[1], self._dXYZ[2] = self._dR*np.cos(self._Theta)*np.sin(self._Phi) - self._R*np.sin(self._Theta)*self._dTheta*np.sin(self._Phi) + self._R*np.sin(self._Theta)*np.cos(self._Phi)*self._dPhi, self._dR*np.sin(self._Theta)*np.sin(self._Phi) + self._R*np.cos(self._Theta)*self._dTheta*np.sin(self._Phi) + self._R*np.sin(self._Theta)*np.cos(self._Phi)*self._dPhi, self._dR*np.cos(self._Phi) - self._R*np.sin(self._Phi)*self._dPhi



    # Funciones para asegurarse que los parametros introducidos son válidos
    @property
    def dF(self):
        return self._dF

    @dF.setter
    def dF(self, func):
        if not callable(func):
            raise exceptions.dFNotCallable(func)
        sig = signature(func)
        if len(sig.parameters)<3 + len(self.dF_args):
            raise exceptions.dFInvalid(sig, self.dF_args)
        self._dF = func

    @property
    def Rango(self):
        return self._Rango

    @Rango.setter
    def Rango(self, value):
        self._Rango = np.array(utils.construct_interval(value, dim=3))


    @property
    def L(self):
        return self._L

    @L.setter
    def L(self, value):
        self._L=value
        if utils.is_number(value):
            self._L = [value for _ in range(self.dimension)]
        while len(self._L)<self.dimension:
            self._L.append(3)


    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise exceptions.dF_argsInvalid(value)
        self._dF_args = value