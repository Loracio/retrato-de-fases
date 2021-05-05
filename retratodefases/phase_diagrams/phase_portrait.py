from inspect import signature

from ..exceptions import exceptions
from ..sliders import sliders
from ..utils import utils

import matplotlib
import matplotlib.pyplot as plt

import numpy as np


class PhasePortrait:
    """
    Base class for N-dimensional phase portraits 
    """
    _name_ = ''
    def __init__(self, dF, Range, dimension, *, MeshDim=20, dF_args={}, Density = 1, Polar = False, Title = 'Phase Portrait', color='rainbow'):
        self.dimension = dimension                       # Dimension of the phase space
        self.dF_args = dF_args                           # dF function's args
        self.dF = dF                                     # Function containing system's equations
        self.Range = Range                               # Range of graphical representation
        
        
        self.L = int(MeshDim)                                            # Number of points in the meshgrid
        self.Density = Density                                           # Controls concentration of nearby trajectories
        self.Polar = Polar                                               # If dF expression given in polar coord. mark as True
        self.Title = Title                                               # Title of the plot

        # Variables for plotting
        self.color = color
        self.sliders = {}
          
            
    
    def draw_plot(self, *, color=None):
        """
        Must plots the values. Must treat `PhasePortrait.Polar=True`
        """
        try:
            for func in self.funcions:
                func.plot()
        except AttributeError:
            pass
            
            
    def plot(self, *, color=None):
        self.draw_plot(color=color if color is not None else self.color)

    
    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Adds a slider on an existing plot
        """
        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.fig.subplots_adjust(bottom=0.25)

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])
        
    
    def update_dF_args(self):
        self.dF_args = {name: slider.value for name, slider in self.sliders.items() if slider.value!= None}  
        
        
    @property
    def dF(self):
        return self._dF

    @dF.setter
    def dF(self, func):
        if not callable(func):
            raise exceptions.dFNotCallable(func)
        sig = signature(func)
        if len(sig.parameters)<self.dimension + len(self.dF_args):
            raise exceptions.dFInvalid(sig, self.dF_args)
        self._dF = func

    @property
    def Range(self):
        return self._Range


    @Range.setter
    def Range(self, value):
        self._Range = np.array(utils.construct_interval(value, dim=2))

    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise exceptions.dF_argsInvalid(value)
        self._dF_args = value