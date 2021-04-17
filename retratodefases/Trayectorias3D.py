import random
from inspect import signature

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from . import sliders
from .exceptions import *
from .utils import utils


class Trayectoria3D:
    """
    Computa una trayectoria en un sistema 3D.
    """
    _name_ = 'Trayectoria3D'
    def __init__(self, dF, *, RangoRepresentacion=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, **kargs):
        """
        Inicializador de clase: inicializa las variables de la clase a los valores pasados. 
        También se definen las variables que se emplean internamente en la clase para realizar el diagrama.
        Se le debe pasar obligatoriamente una función que contenga la expresión de las derivadas de los parámetros.
        """

        # Variables obligatorias
        self.dF_args = dF_args                           # Argumentos extras que haya que proporcionar a la función dF
        self.dF = dF                                     # Derivadas de las variables respecto al tiempo
        self.Rango = RangoRepresentacion                 # Rango de representación del diagrama
        self._dimension = 3

        self.values = []
        self.velocity = []
        self.initial_conditions = []

        try: 
            if kargs['numba']:
                import numba as _numba
                from numba import jit, vectorize
                self.dF = jit(self.dF, nopython=True, cache=True, parallel=True)
                if not dF_args:
                    exceptions.dFArgsRequired()
        except KeyError:
            pass


        # Variables Runge-Kutta
        self.runge_kutta_step = runge_kutta_step
        self.runge_kutta_freq = runge_kutta_freq
        self.n_points = n_points
        
        # Variables no obligatorias
        self.Titulo = kargs['Titulo'] if kargs.get('Titulo') else 'Trayectoria'             # Titulo para el retrato de fases.
        self.xlabel = kargs['xlabel'] if kargs.get('xlabel') else 'X'                       # Titulo en eje X
        self.ylabel = kargs['ylabel'] if kargs.get('ylabel') else 'Y'                       # Titulo en eje Y
        self.zlabel = kargs['zlabel'] if kargs.get('zlabel') else 'Z'                       # Titulo en eje Z


        # Variables para la representación
        figX, axX= plt.subplots()
        figY, axY= plt.subplots()
        figZ, axZ= plt.subplots()
        fig3d = plt.figure()
        ax3d = fig3d.add_subplot(projection='3d')

        self.fig = {
            'X': figX,
            'Y': figY,
            'Z': figZ,
            '3d': fig3d
        }
        self.ax = {
            'X': axX,
            'Y': axY,
            'Z': axZ,
            '3d': ax3d
        }
        
        self.sliders = {}
        self.sliders_fig = False

        self.lines = kargs.get('lines')

        self.termalization = kargs.get('termalization')
        if not self.termalization:
            self.termalization = 0
        self.size = kargs.get('size')
        if not self.size:
            self.size = 0.5
        self.color = kargs.get('color')
        self._mark_start_point = kargs.get('mark_start_point')


    def _create_sliders_plot(self):
        if not isinstance(self.sliders_fig, plt.Figure):
            self.sliders_fig, self.sliders_ax = plt.subplots() 
            self.sliders_ax.set_visible(False)


    def rungekutta_time_independent(self, initial_values):
        values = initial_values
        if not isinstance(values, np.ndarray):
            values = np.array(values)
        while True:
            k1 = np.array(self.dF(*(values), **self.dF_args))
            k2 = np.array(self.dF(*(values+0.5*k1*self.runge_kutta_step), **self.dF_args))
            k3 = np.array(self.dF(*(values+0.5*k2*self.runge_kutta_step), **self.dF_args))
            k4 = np.array(self.dF(*(values+k3*self.runge_kutta_step), **self.dF_args))
            diff = 1/6*self.runge_kutta_step*(k1+2*k2+2*k3+k4)
            values += diff
            yield values, diff


    def compute_trayectory(self, initial_values):
        values = np.zeros([3,self.n_points])
        velocity = np.zeros([3,self.n_points])

        try:
            values[:,0] = np.array(initial_values)
        except:
            values[:,0] = np.array([random.random(), random.random(), random.random()])
        
        for i in range(1, self.n_points + self.termalization):
            for j in range(self.runge_kutta_freq):
                new_value = next(self.rungekutta_time_independent(values[:,0]))
            if i>=self.termalization:
                values[:,i-self.termalization], velocity[:,i-self.termalization] = new_value

        return values, velocity
        
    def termaliza(self):
        self.posicion_inicial()

    def posicion_inicial(self, *args, **kargs):
        if len(args)>0:
            args = np.array(tuple(map(float,args)))
        else:
            args = np.array([random.random(), random.random(), random.random()])

        for vali_init in self.initial_conditions:
            for a, b in zip(args, vali_init):
                if a!=b:
                    break
        else:
            self.initial_conditions.append(args) 
        
    def _calculate_values(self, *args, all_initial_conditions=False, **kargs):
        if not args or all_initial_conditions:
            self.values = []
            self.velocity = []
            if self.initial_conditions:
                for initals in self.initial_conditions:
                    values, velocity = self.compute_trayectory(initals)
                    self.values.append(values)
                    self.velocity.append(velocity)
                return
        values, velocity = self.compute_trayectory(args)
        self.values.append(values)
        self.velocity.append(velocity)
        


    def plot(self, *args, **kargs):
        self._prepare_plot()
        self.dF_args.update({name: slider.value for name, slider in self.sliders.items() if slider.value!= None})

        self._calculate_values(all_initial_conditions=True)

        cmap = kargs.get('color')

        for val, vel, val_init in zip(self.values, self.velocity, self.initial_conditions):
            if self.lines:
                    self.ax['3d'].plot3D(*val[:,1:], label=f"({','.join(tuple(map(str, val_init)))})")
                    self.ax['X'].plot(val[1,1:], val[2,1:], label=f"({','.join(tuple(map(str, val_init)))})")
                    self.ax['Y'].plot(val[0,1:], val[2,1:], label=f"({','.join(tuple(map(str, val_init)))})")
                    self.ax['Z'].plot(val[0,1:], val[1,1:], label=f"({','.join(tuple(map(str, val_init)))})")
            else:
                def norma(v):
                    suma = 0
                    for i in range(3):
                        suma += np.nan_to_num(v[i]**2)
                    return np.sqrt(suma)
                if self.color == 't':
                    color = np.linspace(0,1, vel.shape[1])
                else:
                    cmap = self.color
                    color = norma(vel[:])
                    color /= color.max()

                self.ax['3d'].scatter3D(*val, s=self.size, c=color, cmap=cmap)
                self.ax['X'].scatter(val[1,:], val[2,:], s=self.size, c=color, cmap=cmap)
                self.ax['Y'].scatter(val[0,:], val[2,:], s=self.size, c=color, cmap=cmap)
                self.ax['Z'].scatter(val[0,:], val[1,:], s=self.size, c=color, cmap=cmap)

            if self._mark_start_point:
                for point in self.initial_conditions:
                    self.ax['3d'].scatter3D(*point, s=self.size+1, c=[0])
                    self.ax['X'].scatter(point[1], point[2], s=self.size+1, c=[0])
                    self.ax['Y'].scatter(point[0], point[2], s=self.size+1, c=[0])
                    self.ax['Z'].scatter(point[0], point[1], s=self.size+1, c=[0])

        for fig in self.fig.values():
            if self.lines:
                fig.legend()
            fig.canvas.draw_idle()
        try:
            self.sliders_fig.canvas.draw_idle()
        except:
            pass

    def _prepare_plot(self):
        self.ax['3d'].set_title(f'{self.Titulo}')
        if self.Rango is not None:
            self.ax['3d'].set_xlim(self.Rango[0,:])
            self.ax['3d'].set_ylim(self.Rango[1,:])
            self.ax['3d'].set_zlim(self.Rango[2,:])
        self.ax['3d'].set_xlabel(f'{self.xlabel}')
        self.ax['3d'].set_ylabel(f'{self.ylabel}')
        self.ax['3d'].set_zlabel(f'{self.zlabel}')
        self.ax['3d'].grid()

        for coord, r0, r1, title, x_label, y_label in [
            ('X', 1, 2, 'YZ', self.ylabel, self.zlabel),
            ('Y', 0, 2, 'XZ', self.xlabel, self.zlabel),
            ('Z', 0, 1, 'XY', self.xlabel, self.ylabel),
        ]:

            self.ax[coord].set_title(f'{self.Titulo}: {title}')
            if self.Rango is not None:
                self.ax[coord].set_xlim(self.Rango[r0,:])
                self.ax[coord].set_ylim(self.Rango[r1,:])
            self.ax[coord].set_xlabel(f'{x_label}')
            self.ax[coord].set_ylabel(f'{y_label}')
            self.ax[coord].grid()


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
            if len(sig.parameters)<3 + len(self.dF_args):
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
