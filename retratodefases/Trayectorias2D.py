import random
from inspect import signature

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from .trajectories import trajectory as trj

class Trayectoria2D(trj.trajectory):
    """
    Computa una trayectoria en un sistema 3D.
    """
    _name_ = 'Trayectoria2D'
    def __init__(self, dF, *, RangoRepresentacion=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, **kargs):
        """
        Inicializador de clase: inicializa las variables de la clase a los valores pasados. 
        También se definen las variables que se emplean internamente en la clase para realizar el diagrama.
        Se le debe pasar obligatoriamente una función que contenga la expresión de las derivadas de los parámetros.
        """
        super().__init__(dF, 2, RangoRepresentacion=RangoRepresentacion, dF_args=dF_args, n_points=n_points, runge_kutta_step=runge_kutta_step, runge_kutta_freq=runge_kutta_freq, **kargs)

        # Variables no obligatorias
        self.xlabel = kargs['xlabel'] if kargs.get('xlabel') else 'X'                       # Titulo en eje X
        self.ylabel = kargs['ylabel'] if kargs.get('ylabel') else 'Y'                       # Titulo en eje Y


        # Variables para la representación
        figZ, axZ= plt.subplots()

        self.fig = {
            'Z': figZ,
        }
        self.ax = {
            'Z': axZ,
        }


    def _plot_lines(self, val, val_init):
        self.ax['Z'].plot(val[0,1:], val[1,1:], label=f"({','.join(tuple(map(str, val_init)))})")


    def _scatter_start_point(self, val_init):
        self.ax['Z'].scatter(val_init[0], val_init[1], s=self.size+1, c=[0])


    def _scatter_trajectory(self, val, color, cmap):
        self.ax['Z'].scatter(val[0,:], val[1,:], s=self.size, c=color, cmap=cmap)


    def _prepare_plot(self):
        for coord, r0, r1, x_label, y_label in [
            ('Z', 0, 1, self.xlabel, self.ylabel),
        ]:

            self.ax[coord].set_title(f'{self.Titulo}')
            if self.Rango is not None:
                self.ax[coord].set_xlim(self.Rango[r0,:])
                self.ax[coord].set_ylim(self.Rango[r1,:])
            self.ax[coord].set_xlabel(f'{x_label}')
            self.ax[coord].set_ylabel(f'{y_label}')
            self.ax[coord].grid()