from inspect import signature

import matplotlib.pyplot as plt
import numpy as np

from .exceptions import exceptions
from .phase_diagrams import Funcion1D
from .sliders import sliders
from .utils import utils


class Cobweb:
    """
    Cobweb
    ------
    Class dedicated cobweb plots of 1 dimension maps `x(t+1) = f(x)`.
    
    Methods
    -------
    plot :
        Prepares the plots, compute the values, and plots them. 
        Returns the axis and the figure.
        
    add_slider :
        Adds a `Slider` for the `dF` funcion.
        
    initial_position_slider :
        Adds a slider for changing the initial value.
        
    add_funcion : 
        Adds a funcion to the Cobweb plot.
    """

    _name_ = 'Cobweb'
    def __init__(self, dF, initial_position, xrange, *, dF_args={None}, yrange=[], max_steps=100, n_points=100, **kargs):
        """
        Cobweb
        ------
        Parameters
        ----------
        dF : callable
            A dF type funcion.
        initial_position : float
            Initial x of the iteration.
        xrange : list
            Range of the x axis in the main plot.
            
        Key Arguments
        -------------
        dF_args : dict
            If necesary, must contain the kargs for the `dF` funcion.
        yrange : list
            Range of the y axis in the main plot
        max_steps : int
            Maximun number of poits to be represented.
        n_points : int
            Number of points in the bisector. 
        Title : str
            Title of the plot.
        xlabel : str
            x label of the plot.
        ylabel : str
            y label of the plot.
        """
        self.dF = dF
        self.dF_args = dF_args
        self.initial_position = initial_position 
        self.xrange = xrange

        self.yrange = yrange
        self.max_steps = max_steps
        self.n_points = n_points

        self.Title = kargs['Title'] if kargs.get('Title') else 'Cobweb plot'
        self.xlabel = kargs['xlabel'] if kargs.get('xlabel') else r'$X_n$'
        self.ylabel = kargs['ylabel'] if kargs.get('ylabel') else r'$X_{n+1}$'

        self.fig, self.ax = plt.subplots()
        self.sliders = {}
        self.funcions = []
        self.sliders_fig = False



    def _prepare_plot(self, max_value):

        self.ax.set_title(self.Title)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)

        if self.yrange==[]:
            self.ax.set_ylim(top=1.10*max_value)
        else:
            self.ax.set_ylim(self.yrange)

        self.ax.grid()
    


    def plot(self, *args, **kargs):
        """
        Prepares the plots, compute the values and plots them.
        
        Returns
        -------
        tuple(matplotlib Figure, matplotlib Axis)
        """
        for func in self.funcions:
            func.plot()

        bisector = np.linspace(self.xrange[0], self.xrange[1], self.n_points)
        func_result = self.dF(bisector, **self.dF_args)

        self._prepare_plot(np.max(func_result))

        self.ax.plot(bisector, func_result, 'b')
        self.ax.plot(bisector, bisector, "k:")

        x, y = self.initial_position, self.dF(self.initial_position, **self.dF_args)
        self.ax.plot([x, x], [0, y], 'black')

        for _ in range(self.max_steps):

            self.ax.plot([x, y], [y, y], 'black')
            self.ax.plot([y, y], [y, self.dF(y, **self.dF_args)], 'black')
            x, y = y, self.dF(y, **self.dF_args)

            if y>self.xrange[1] or y<self.xrange[0]:
                print(f'Warning: cobweb plot got out of range and could not compute {self.max_steps} steps.')
                break
            
        self.fig.canvas.draw_idle()
        
        return self.fig, self.ax



    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Adds a slider on an existing plot.
        
        Parameters
        ----------
        param_name : str
            The string key of the variable. Must be the same as the key in the `dF` funcion.
        
        Key Arguments
        -------------
        valinit : float
            Initial value of the parameter.
        valinterval : Union[float, list]
            The range of values the slider of the parameter will cover.
        valstep : float
            Precision in the slider.
        """
        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.fig.subplots_adjust(bottom=0.25)

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])


    def add_funcion(self, funcion1d, *, n_points=500, xRange=None, dF_args=None, color='g'):
        """
        Adds a funcion to the cobweb plot.
    
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
        """ 
        self.funcions.append(Funcion1D(self, funcion1d, n_points=n_points, xRange=xRange, dF_args=None, color=color))
        

    def update_dF_args(self):
        for name, slider in self.sliders.items():
            if slider.value!= None and name!=r'$x_0$':
                self.dF_args[name] = slider.value 

        if self.sliders.get(r'$x_0$'):
            self.initial_position = self.sliders[r'$x_0$'].value

    def initial_position_slider(self, *, valstep=0.05, valinterval=[0,1]):
        """
        Adds a slider for changing initial value on a cobweb plot.
        
        Key Arguments
        -------------
        valinterval : Union[float, list]
            The range of values the slider of the parameter will cover.
        valstep : float
            Precision in the slider.
        """
        self.sliders.update({r'$x_0$': sliders.Slider(self, r'$x_0$', valinit=self.initial_position, valstep=valstep, valinterval=valinterval)})

        self.fig.subplots_adjust(bottom=0.25)

        self.sliders[r'$x_0$'].slider.on_changed(self.sliders[r'$x_0$'])


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
        self._dF = func

    @property
    def xrange(self):
        return self._xrange

    @xrange.setter
    def xrange(self, value):
        if value == None:
            self._xrange = None
            return
        self._xrange = np.array(utils.construct_interval(value, dim=1))

    @property
    def yrange(self):
        return self._yrange

    @yrange.setter
    def yrange(self, value):
        if value == None:
            self._yrange = None
            return
        self._yrange = np.array(utils.construct_interval(value, dim=1))

    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise exceptions.dF_argsInvalid(value)
        self._dF_args = value
