from inspect import signature

from .exceptions import exceptions
from .sliders import sliders
from .utils import utils

from .phase_diagrams import PhasePortrait, Funcion1D
import matplotlib
import matplotlib.pyplot as plt

import numpy as np

class RetratoDeFases2D(PhasePortrait):
    """
    Hace un retrato de fases de un sistema 2D.
    """
    _name_ = 'RetratoDeFases2D'
    def __init__(self, dF, RangoRepresentacion, *, LongitudMalla=10, dF_args={}, Densidad = 1, Polar = False, Titulo = 'Retrato de Fases', xlabel = 'X', ylabel = r"$\dot{X}$", color='rainbow'):
        """
        Inicializador de clase: inicializa las variables de la clase a los valores pasados. 
        También se definen las variables que se emplean internamente en la clase para realizar el diagrama.
        Se le debe pasar obligatoriamente una función que contenga la expresión de las derivadas de los parámetros.
        """
        super().__init__(dF, RangoRepresentacion, 2, MeshDim=LongitudMalla, dF_args=dF_args, Polar=Polar, Title=Titulo, color=color)
        
        # Variables no obligatorias                                                           # Titulo para el retrato de fases.
        self.xlabel = xlabel                                                                  # Titulo en eje X
        self.ylabel = ylabel                                                                  # Titulo en eje Y

        # Variables para la representación
        self.fig, self.ax = plt.subplots()
        self.funcions = []

        # Variables que el usuario no debe emplear: son para el tratamiento interno de la clase. Es por ello que llevan el prefijo "_"
        self._X, self._Y = np.meshgrid(np.linspace(*self.Range[0,:], self.L), np.linspace(*self.Range[1,:], self.L))   #Crea una malla de tamaño L²

        if self.Polar:   
            self._R, self._Theta = (self._X**2 + self._Y**2)**0.5, np.arctan2(self._Y, self._X) # Transformacion de coordenadas cartesianas a polares

    def add_funcion(self, funcion1d, *, n_points=500, xRange=None, dF_args=None, color='g'):
        self.funcions.append(Funcion1D(self, funcion1d, n_points=n_points, xRange=xRange, dF_args=None, color=color))
        

    def plot(self, *, color=None):
        self.draw_plot(color=color)
        self.fig.canvas.draw_idle()


    def draw_plot(self, *, color=None):
        if self.Polar:
            self._transformacionPolares()
        else:
            self._dX, self._dY = self.dF(self._X, self._Y, **self.dF_args)
            
        for func in self.funcions:
            func.plot()
            
        colores = (self._dX**2+self._dY**2)**(0.5)
        colores_norm = matplotlib.colors.Normalize(vmin=colores.min(), vmax=colores.max())
        stream = self.ax.streamplot(self._X, self._Y, self._dX, self._dY, color=colores, cmap=color, norm=colores_norm, linewidth=1, density= self.Density)
        self.ax.set_xlim(self.Range[0,:])
        self.ax.set_ylim(self.Range[1,:])
        x0,x1 = self.ax.get_xlim()
        y0,y1 = self.ax.get_ylim()
        self.ax.set_aspect(abs(x1-x0)/abs(y1-y0))
        self.ax.set_title(f'{self.Title}')
        self.ax.set_xlabel(f'{self.xlabel}')
        self.ax.set_ylabel(f'{self.ylabel}')
        self.ax.grid()
        
        return stream
    
    
    def _transformacionPolares(self):
        """
        Devuelve la expresión del campo de velocidades en cartesianas, si la expresión del sistema viene dada en polares
        """
        self._dR, self._dTheta = self.dF(self._R, self._Theta, **self.dF_args)
        self._dX, self._dY = self._dR*np.cos(self._Theta) - self._R*np.sin(self._Theta)*self._dTheta, self._dR*np.sin(self._Theta)+self._R*np.cos(self._Theta)*self._dTheta