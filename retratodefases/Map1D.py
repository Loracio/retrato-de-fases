from inspect import Attribute
import matplotlib
import numpy as np
from matplotlib import pyplot as plt

from .maps import Map
from .sliders import Slider
from .phase_diagrams import Funcion1D

class Map1D():
    '''
    Map1D
    --------
    
    Parameters
    ----------
    dF : callable
        A dF type funcion.
    Range : [x_range, y_range]
        Ranges of the axis in the main plot.
    n_points : int
        Maximum number of points
    
    Key Arguments
    -----
    dF_args : dict
        If necesary, must contain the kargs for the `dF` funcion.
    composition_grade : int
        Number of times `dF` is aplied between positions saved.
    Titulo : str
        Title of the plot.
    xlabel : str
        x label of the plot.
    ylabel : str
        y label of the plot.
    color : str
        Matplotlib `Cmap`.
    size : float
        Size of the scattered points.
    thermalization : int
        Thermalization steps before points saved.
    
    Methods
    -------
    plot_over_variable : 
        Creates every `map` instance.
    
        param_name : str
            Name of the variable. Must be in the `dF` kargs.
        valinterval : list
            Min and max value for the param range.
        valstep : float
            Separation between consecutive values in the param range.
            
    plot_trajectory : 
        Creates a `map` instance and computes it's positions.
        Returns : `plt.Figure` , `plt.Axis`
        
        n_points : int
            Number of points to be calculated.
    
    add_funcion : 
        Adds a funcion to the `dF` plot.
    
        funcion1d : callable
            A dF type funcion.
    
    add_slider :
        Adds a `Slider` for the `dF` funcion.
    
        param_name : str
            Name of the variable. Must be in the `dF` kargs of the `Map1D.dF` funcion.
            
    plot :
        Prepares the plots and computes the values.
        
    '''
    
    _name_ = 'Map1D'

    def __init__(self, dF, x_range, y_range, n_points, *, composition_grade=1, dF_args={}, Titulo='Mapa 1D', xlabel=r'control parameter', ylabel=r'$X_{n+1}$', **kargs):
        self.dF_args = dF_args
        self.dF = dF
        self.Range = np.array([x_range, y_range])
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

        self.sliders = {}
        
        self.funcions = []
        
        self._trajectory = None

        self.size = kargs.get('size')
        if self.size is None:
            self.size = 1
        self.thermalization = kargs.get('thermalization')
        
        self._initial_x = sum(self.Range[1])/2

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
        '''
        plot_over_variable : 
        Creates every `map` instance.
    
        Parameters
        ---------
        param_name : str
            Name of the variable. Must be in the `dF` kargs.
        valinterval : list
            Min and max value for the param range.
        valstep : float
            Separation between consecutive values in the param range.
            
        Key Arguments
        ------------
        initial_x : float
            Initial x position of every data series.
        limit_cicle_check_first : int
            Number of points saved before checking for repeated elemets.
        delta_cicle_check : float
            Diference between two positions to be considerated identical.
        
        
        '''
        self._param_name = param_name
        self._valinterval = valinterval
        if initial_x is None:
            initial_x = self._initial_x
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
        '''
        Prepares the plots and computes the values.
        
        Key Arguments
        -------------
        color : str
            Matplotlib `Cmap`.
        
        '''
        for func in self.funcions:
            func.plot()
        
        self._compute_data()

        if color is not None:
            self.color = color

        for i in self._range:
            values = self.maps[i].positions
            color = values[0, 0:-2]
            range_x = np.zeros(len(color)) + i
            self.ax.scatter(
                range_x, values[0, 1:-1],
                s=self.size, c=color, cmap=self._cmap, norm=self._colores_norm
            )

    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        '''
        Adds a `Slider` for the `dF` funcion.
    
        Parameters
        ---------
        param_name : str
            Name of the variable. Must be in the `dF` kargs of the `Map1D.dF` funcion.
        
        Key Arguments
        ------------
        valinit : float
            Initial position of the Slider
        valinterval : list
            Min and max value for the param range.
        valstep : float
            Separation between consecutive values in the param range.

        ''' 
        self.sliders.update({param_name: Slider(
            self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.fig.subplots_adjust(bottom=0.25)

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])

    def add_funcion(self, funcion1d, *, n_points=500, xRange=None, dF_args=None, color='g'):
        '''
        Adds a funcion to the `dF` plot.
    
        Parameters
        ---------
        funcion1d : callable
            A dF type funcion.
        
        Key Arguments
        ------------
        n_points : int
            Number of points in the funcion representation.
        xRange : list
            The x range in which the points are calculated.
        dF_args : dict
            If necesary, must contain the kargs for the `dF` funcion.
        color : str 
            String  matplotlib color identifier.
        ''' 
        self.funcions.append(Funcion1D(self, funcion1d, n_points=n_points, xRange=xRange, dF_args=None, color=color))
        

    def _prepare_plot_trajectory(self):
        if self._trajectory is None:
            self._trajectory = plt.subplots()
        self._trajectory[1].cla()
        self._trajectory[1].set_title(f'{self.Titulo}: {self.xlabel}={self._param_name}')
        self._trajectory[1].set_ylim(*self.Range[1])
        self._trajectory[1].set_xlabel('t')
        self._trajectory[1].set_ylabel(r'$X_{n}$')
        self._trajectory[1].grid()

        
    def plot_trajectory(self, n_points, *, dF_args=None, initial_x=None, color='b', save_freq=1, thermalization=0):
        '''
        Creates a `map` instance and computes it's positions.
        
        Returns : `plt.Figure` , `plt.Axis`
        
        Parameters
        ----------
        n_points : int
            Number of points to be calculated.
            
        Key Arguments
        -----
        dF_args : dict
            If necesary, must contain the kargs for the `dF` funcion. By default takes the dF_args of the `Map1D` instance.
        initial_x : float
            Initial position of the trajectory.
        color : str
            String  matplotlib color identifier.
        save_freq : int
            Number of times `dF` is aplied before a position is saved.
        thermalization : int
            Thermalization steps before points saved.
        '''
        try:
            if self._param_name:
                pass
        except AttributeError:
            print('Method plot_over_variable must be executed before.')
            return
        
        if dF_args is None:
            dF_args = self.dF_args
        if initial_x is None:
            initial_x = self._initial_x
    
        self._prepare_plot_trajectory()
        s_map = Map.instance_and_compute_all(None, self.dF, self.dimension, n_points, dF_args=dF_args, initial_values=initial_x, save_freq=save_freq, thermalization=thermalization)
        self._trajectory[1].plot(s_map.positions[0], '.-', color=color)
        return self._trajectory