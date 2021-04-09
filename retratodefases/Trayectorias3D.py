from inspect import signature

from .exceptions import *
from . import sliders
from .utils import utils

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numba
from numba import jit

import numpy as np

# TODO: Falta cambiar nombres y documentación. Y evidentemente quitar cosas que ya no se usan


class Trayectoria3D:
    """
    Hace un retrato de fases de un sistema 3D.
    """
    def __init__(self, dF, RangoRepresentacion, dF_args, *, Polar = False, Titulo = 'Retrato de Fases', xlabel = 'X', ylabel = 'Y', zlabel = 'Z'):
        """
        Inicializador de clase: inicializa las variables de la clase a los valores pasados. 
        También se definen las variables que se emplean internamente en la clase para realizar el diagrama.
        Se le debe pasar obligatoriamente una función que contenga la expresión de las derivadas de los parámetros.
        """

        # Variables obligatorias
        self.dF_args = dF_args                           # Argumentos extras que haya que proporcionar a la función dF
        self.dF = jit(dF, nopython=True, parallel=True)  # Derivadas de las variables respecto al tiempo
        self.Rango = RangoRepresentacion                 # Rango de representación del diagrama
        self.dimension = 3

        self.h = 0.01

        # Variables Runge-Kutta
        self.runge_freq = 5
        self._runge_inner_steps = 100
        self.max_iters = 5
        
        # Variables no obligatorias
        self.Titulo = Titulo                                                                  # Titulo para el retrato de fases.
        self.xlabel = xlabel                                                                  # Titulo en eje X
        self.ylabel = ylabel                                                                  # Titulo en eje Y
        self.zlabel = zlabel                                                                  # Titulo en eje Z


        # Variables para la representación
        #self.fig, self.ax = plt.subplots()
        self.fig, ((self.ax3d, self.axZ), (self.axY, self.axX)) = plt.subplots(2,2)
        #self.ax = self.fig.add_subplot(projection='3d')
        self.sliders = {}

        # Variables que el usuario no debe emplear: son para el tratamiento interno de la clase. Es por ello que llevan el prefijo "_"
        #! elf._X, self._Y = np.meshgrid(np.linspace(*self.Rango[0,:], self.L), np.linspace(*self.Rango[1,:], self.L))   #Crea una malla de tamaño L²
        #self._XYZ = np.meshgrid(*[np.linspace(*r, l) for r, l in zip(self.Rango, self.L)])

        #! Falta arreglar esto para tres coordenadas. Me da pereza
        #if self.Polar:   
        #    self._R, self._Theta = (self._X**2 + self._Y**2)**0.5, np.arctan2(self._Y, self._X) # Transformacion de coordenadas cartesianas a polares


    def rungekutta_time_independent(self, initial_values):
        initial_values = np.array(initial_values, dtype='float64')
        results = np.zeros([len(initial_values), self.runge_freq])
        results[:,0]= initial_values
        for i in range(1, self.runge_freq*self._runge_inner_steps):
            k1 = np.array(self.dF(*(initial_values), **self.dF_args))
            k2 = np.array(self.dF(*(initial_values+0.5*k1*self.h), **self.dF_args))
            k3 = np.array(self.dF(*(initial_values+0.5*k2*self.h), **self.dF_args))
            k4 = np.array(self.dF(*(initial_values+k3*self.h), **self.dF_args))
            initial_values += 1/6*self.h*(k1+2*k2+2*k3+k4)
            if (index := i%self._runge_inner_steps) == 0:
                results[:,index] = initial_values
        return results

    def update_time_independent(self, *initial_values):
        values = np.zeros([3,1])
        values[:,0] = np.array(initial_values)
        
        new_values = self.rungekutta_time_independent(values[:,-1])
        for i in range(values.shape[0]):
            values[i,:] = np.concatenate((values[i,:], new_values[i,:]))
        #initial_values[i+1].append(new_values[i])

        self.ax3d.plot(*values)
        self.axX.plot(*values[1:2])
        self.axY.plot(*values[0:2:2])
        self.axZ.plot(*values[0:1])

    def plot(self, *args):
        self.prepare_plot()
        args = list(args)

        for i in range(self.max_iters):
            self.update_time_independent(args)
            self.fig.canvas.draw_idle()


    #def norma(self):
    #    cuadrado = lambda x: x*x
    #    result = np.zeros(self.L)
    #    for i in self._XYZ:
    #        result += i**2
    #    return result**0.5


    def prepare_plot(self):

        #self.dF_args = {name: slider.value for name, slider in self.sliders.items() if slider.value!= None}

        #if self.Polar:
        #    self._transformacionPolares()
        #else:
        #    #! self._dX, self._dY = self.dF(self._X, self._Y, **self.dF_args)
        #    self._dXYZ = self.dF(*self._XYZ, **self.dF_args)
        #colores = (self._XYZ[0]**2+self._XYZ[1]**2+self._XYZ[2]**2)**(0.5)
        #colores_p = self.norma()
        #colores_norm = matplotlib.colors.Normalize(vmin=colores_p.min(), vmax=colores_p.max())
        #! stream = self.ax.streamplot(self._X, self._Y, self._dX, self._dY, color=colores_p, cmap=color, norm=colores_norm, linewidth=1, density= self.Densidad)
        #stream = self.ax.quiver(*self._XYZ, *self._dXYZ, length=0.1)#, cmap='Reds')

        self.ax3d.set_title(f'{self.Titulo}')
        self.ax3d.set_xlim(self.Rango[0,:])
        self.ax3d.set_ylim(self.Rango[1,:])
        #self.ax3d.set_zlim(self.Rango[2,:])
        self.ax3d.set_xlabel(f'{self.xlabel}')
        self.ax3d.set_ylabel(f'{self.ylabel}')
        #self.ax3d.set_zlabel(f'{self.zlabel}')
        self.ax3d.grid()

        self.axX.set_title(f'{self.Titulo}: YZ')
        self.axX.set_xlim(self.Rango[1,:])
        self.axX.set_ylim(self.Rango[2,:])
        self.axX.set_xlabel(f'{self.ylabel}')
        self.axX.set_ylabel(f'{self.zlabel}')
        self.axX.grid()

        self.axY.set_title(f'{self.Titulo}: XZ')
        self.axY.set_xlim(self.Rango[0,:])
        self.axY.set_ylim(self.Rango[2,:])
        self.axY.set_xlabel(f'{self.xlabel}')
        self.axY.set_ylabel(f'{self.zlabel}')
        self.axY.grid()

        self.axZ.set_title(f'{self.Titulo}: XY')
        self.axZ.set_xlim(self.Rango[0,:])
        self.axZ.set_ylim(self.Rango[1,:])
        self.axZ.set_xlabel(f'{self.xlabel}')
        self.axZ.set_ylabel(f'{self.ylabel}')
        self.axZ.grid()


    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Añade un slider sobre un plot ya existente.
        """
        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.fig.subplots_adjust(bottom=0.25)

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])
    
    
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
            self._L.append(10)


    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise exceptions.dF_argsInvalid(value)
        self._dF_args = value