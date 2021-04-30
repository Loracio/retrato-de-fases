import matplotlib
import numpy as np
from matplotlib import pyplot as plt

from .maps import Map
from .sliders import Slider


class Map1D():
    _name_ = 'Map1D'

    def __init__(self, dF, x_range, y_range, n_points, *, composition_grade=1, dF_args, Titulo='Mapa 1D', xlabel=r'control parameter', ylabel=r'$X_{n+1}$', **kargs):
        self.dF_args = dF_args
        self.dF = dF
        self.Range = x_range, y_range
        self.n_points = n_points
        self.dimension = 1

        self.composition_grade = composition_grade

        self.Titulo = Titulo
        self.xlabel = xlabel
        self.ylabel = ylabel

        # Variables para la representación
        self.fig, self.ax = plt.subplots()
        self.color = kargs.get('color')
        if not self.color:
            self.color = 'inferno'

        self.maps = {}
        #! No se si podríamos implementar sliders aquí, no creo que sea útil, lo dejo por si acaso
        self.sliders = {}
        
        self._trajectory = None

        self.size = kargs.get('size')
        if self.size is None:
            self.size = 1
        self.thermalization = kargs.get('thermalization')

    def _compute_data(self):
        self._range = np.arange(
            self._valinterval[0], self._valinterval[1], self._valstep)


        dF_args = self.dF_args.copy()
        for i, param in enumerate(self._range):
            dF_args.update({self._param_name: param})

            self.maps.update({param: Map.instance_and_compute_all(self, self.dF, self.dimension,
                             self.n_points, dF_args, self._initial_x, thermalization=self.thermalization,
                             limit_cicle_check=self._limit_cicle_check_first, delta=self._delta_cicle_check, save_freq=self.composition_grade)})

    def plot_over_variable(self, param_name, valinterval, valstep, *, initial_x=None, limit_cicle_check_first=50, delta_cicle_check=0.0001):
        self._param_name = param_name
        self._initial_x = initial_x if initial_x is not None else (
            sum(self.Range[0, :])/2)
        self._valinterval = valinterval
        self._valstep = valstep
        self._limit_cicle_check_first = limit_cicle_check_first
        self._delta_cicle_check = delta_cicle_check
        self._prepare_plot()

    def _prepare_plot(self):
        self.ax.set_title(f'{self.Titulo}')
        self._cmap = self.color
        self._colores_norm = plt.Normalize(
            vmin=self.Range[1][0], vmax=self.Range[1][1])
        self.ax.set_xlim(*self.Range[0])
        self.ax.set_ylim(*self.Range[1])
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.grid()
        self.fig.colorbar(matplotlib.cm.ScalarMappable(
            norm=self._colores_norm, cmap=self._cmap), label=r'$X_{n}$')
        
    def update_dF_args(self):
        self.dF_args.update({name: slider.value for name, slider in self.sliders.items() if slider.value!= None})
        

    def plot(self, *, color=None):
        self._compute_data()

        if color is not None:
            self.color = color
            
        if self._trajectory is not None:
            self.plot_trajectory(self.n_points, color=color)

        for i in self._range:
            values = self.maps[i].positions
            color = values[0, 0:-2]
            range_x = np.zeros(len(color)) + i
            self.ax.scatter(
                range_x, values[0, 1:-1],
                s=self.size, c=color, cmap=self._cmap, norm=self._colores_norm
            )

    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        self.sliders.update({param_name: Slider(
            self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.fig.subplots_adjust(bottom=0.25)

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])


    def _prepare_plot_trajectory(self):
        if self._trajectory is None:
            self._trajectory = plt.subplots()
        self._trajectory[1].cla()
        self._trajectory[1].set_title(f'{self.Titulo}: {self.xlabel}={self._param_name}')
        self._trajectory[1].set_ylim(*self.Range[1])
        self._trajectory[1].set_xlabel('t')
        self._trajectory[1].set_ylabel(r'$X_{n}$')
        self._trajectory[1].grid()
        
    def plot_trajectory(self, n_points, *, color='b'):
        
        #TODO: arreglar esto
        
        self._prepare_plot_trajectory()
        s_map = Map(None, self.dF, self.dimension, self.n_points, dF_args=self.dF_args, initial_values=self._initial_x)
        s_map.compute_all()
        self._trajectory[1].plot(s_map.positions[0], '.-', color=color)