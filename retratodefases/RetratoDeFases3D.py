from inspect import signature

from .exceptions import exceptions
from .sliders import sliders
from .utils import utils

from .phase_diagrams import PhasePortrait
#import matplotlib
import matplotlib.pyplot as plt

import numpy as np

class RetratoDeFases3D(PhasePortrait):
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
        super().__init__(dF, RangoRepresentacion, 3, MeshDim=LongitudMalla, dF_args=dF_args, Polar=Polar, Title=Titulo, color=color)
        
        # Variables no obligatorias                                                               # Titulo para el retrato de fases.
        self.xlabel = xlabel                                                                  # Titulo en eje X
        self.ylabel = ylabel                                                                  # Titulo en eje Y
        self.zlabel = zlabel                                                                  # Titulo en eje Z

        # Variables para la representación
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')

        # Variables que el usuario no debe emplear: son para el tratamiento interno de la clase. Es por ello que llevan el prefijo "_"
        self._XYZ = np.meshgrid(*[np.linspace(*r, l) for r, l in zip(self.Rango, self.L)])
        self._dXYZ = []*3

        #* Teóricamente, debería estar arreglado, pero repito, teóricamente. Bueno, es incorrecto por lo que explico en los comentarios de las líneas anteriores, pero sería meterle las componentes de la lista
        if self.Polar:   
            self._R, self._Theta, self._Phi = (self._XYZ[0]**2 + self._XYZ[1]**2 + self._XYZ[2]**2)**0.5, np.arctan2(self._XYZ[1], self._XYZ[0]), np.arctan2(((self._XYZ[0]**2 + self._XYZ[1]**2)**0.5), self._XYZ[2])  # Transformacion de coordenadas cartesianas a esféricas


    def norma(self):
        square = lambda x: x*x
        result = np.zeros(self.L)
        for i in self._XYZ:
            result += i*i
        return np.sqrt(result)


    def draw_plot(self, *, color=None):
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

    
    def _transformacionEsfericas(self):
        """
        Devuelve la expresión del campo de velocidades en cartesianas, si la expresión del sistema viene dada en esféricas
        """
        self._dR, self._dTheta, self._dPhi = self.dF(self._R, self._Theta, self._Phi **self.dF_args)
        self._dXYZ[0], self._dXYZ[1], self._dXYZ[2] = self._dR*np.cos(self._Theta)*np.sin(self._Phi) - self._R*np.sin(self._Theta)*self._dTheta*np.sin(self._Phi) + self._R*np.sin(self._Theta)*np.cos(self._Phi)*self._dPhi, self._dR*np.sin(self._Theta)*np.sin(self._Phi) + self._R*np.cos(self._Theta)*self._dTheta*np.sin(self._Phi) + self._R*np.sin(self._Theta)*np.cos(self._Phi)*self._dPhi, self._dR*np.cos(self._Phi) - self._R*np.sin(self._Phi)*self._dPhi


    # Funciones para asegurarse que los parametros introducidos son válidos
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