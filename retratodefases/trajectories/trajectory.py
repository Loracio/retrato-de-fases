import random
from inspect import signature

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from ..sliders import sliders
from . import RungeKutta
from ..exceptions import exceptions
from ..utils import utils


class trajectory:
    """
    Computa una trayectoria en un sistema 2D o 3D.
    """
    _name_ = 'trajectory'
    def __init__(self, dF, dimension, *, RangoRepresentacion=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, **kargs):
        """
        Inicializador de clase: inicializa las variables de la clase a los valores pasados. 
        También se definen las variables que se emplean internamente en la clase para realizar el diagrama.
        Se le debe pasar obligatoriamente una función que contenga la expresión de las derivadas de los parámetros.
        """

        # Variables obligatorias
        self._dimension = dimension
        self.dF_args = dF_args                           # Argumentos extras que haya que proporcionar a la función dF
        self.dF = dF                                     # Derivadas de las variables respecto al tiempo
        self.Rango = RangoRepresentacion                 # Rango de representación del diagrama

        try: 
            if kargs['numba']:
                from numba import jit
                self.dF = jit(self.dF, nopython=True)
                if not dF_args:
                    exceptions.dFArgsRequired()
        except KeyError:
            pass

        # Variables Runge-Kutta generales
        self.runge_kutta_step = runge_kutta_step
        self.runge_kutta_freq = runge_kutta_freq
        self.n_points = n_points
        self.trajectories = []
        
        # Variables no obligatorias
        self.Titulo = kargs['Titulo'] if kargs.get('Titulo') else 'Trayectoria'             # Titulo para el retrato de fases.
        
        self.sliders = {}
        self.sliders_fig = False

        self.lines = kargs.get('lines')

        self.thermalization = kargs.get('thermalization')
        if not self.thermalization:
            self.thermalization = 0
        self.size = kargs.get('size')
        if not self.size:
            self.size = 0.5
        self.color = kargs.get('color')
        self._mark_start_point = kargs.get('mark_start_point')

    # Funciones que deben ser sobreescritas en clases que hereden de esta
    def _prepare_plot(self):...
    def _scatter_start_point(self, val_init):...
    def _scatter_trajectory(self, val, color, cmap):...
    def _plot_lines(self, val, val_init):...


    # Funciones generales
    def _create_sliders_plot(self):
        if not isinstance(self.sliders_fig, plt.Figure):
            self.sliders_fig, self.sliders_ax = plt.subplots() 
            self.sliders_ax.set_visible(False)

        
    def termaliza(self):
        self.posicion_inicial()


    def posicion_inicial(self, *args, **kargs):
        flag = False
        for trajectory in self.trajectories:
            for a, b in zip(args, trajectory.initial_value):
                if a!=b:
                    flag = True
        
        if not flag and len(self.trajectories)>0:
            return
        
        self.trajectories.append(
            RungeKutta(
                self, self.dF, self._dimension, self.n_points, 
                dt=self.runge_kutta_step,
                dF_args=self.dF_args, 
                initial_values=args,
                thermalization=self.thermalization
                )
            )
 
        
    def _calculate_values(self, *args, all_initial_conditions=False, **kargs):
        for trajectory in self.trajectories:
            trajectory.compute_all(save_freq=self.runge_kutta_freq)


    def plot(self, *args, **kargs):
        self._prepare_plot()
        self.dF_args.update({name: slider.value for name, slider in self.sliders.items() if slider.value!= None})
        for trajectory in self.trajectories:
            trajectory.dF_args = self.dF_args
        
        self._calculate_values(all_initial_conditions=True)

        cmap = kargs.get('color')

        for trajectory in self.trajectories:
            val = trajectory.positions
            vel = trajectory.velocities
            val_init = trajectory.initial_value
            
            if self.lines:
                self._plot_lines(val, val_init)
                    
            else:
                def norma(v):
                    suma = 0
                    for i in range(self._dimension):
                        suma += np.nan_to_num(v[i]**2)
                    return np.sqrt(suma)
                if self.color == 't':
                    color = np.linspace(0,1, vel.shape[1])
                else:
                    cmap = self.color
                    color = norma(vel[:])
                    color /= color.max()

                self._scatter_trajectory(val, color, cmap)

            if self._mark_start_point:
                self._scatter_start_point(val_init)
                
        for fig in self.fig.values():
            if self.lines:
                fig.legend()
            fig.canvas.draw_idle()
        try:
            self.sliders_fig.canvas.draw_idle()
        except:
            pass


    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Añade un slider sobre un plot ya existente.
        """
        self._create_sliders_plot()
        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])
    
    
    # Funciones para asegurarse que los parametros introducidos son válidos
    @property
    def dF(self):
        return self._dF

    @dF.setter
    def dF(self, func):
        if not callable(func):
            raise exceptions.dFNotCallable(func)
        try:
            sig = signature(func)
        except ValueError:
            pass
        else:
            if len(sig.parameters)<self._dimension + len(self.dF_args):
                raise exceptions.dFInvalid(sig, self.dF_args)
        self._dF = func


    @property
    def Rango(self):
        return self._Rango

    @Rango.setter
    def Rango(self, value):
        if value == None:
            self._Rango = None
            return
        self._Rango = np.array(utils.construct_interval(value, dim=3))


    @property
    def L(self):
        return self._L

    @L.setter
    def L(self, value):
        self._L=value
        if utils.is_number(value):
            self._L = [value for _ in range(self._dimension)]
        while len(self._L)<self._dimension:
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
