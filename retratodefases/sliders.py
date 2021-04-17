import numpy as np

from .exceptions import *
from .utils import utils
from matplotlib.widgets import Slider as matplot_slider

class Slider():
    def __init__(self, retrato, param_name, valinit=None, valstep=0.1, valinterval=[]):
        self.retrato = retrato
        self.param_name = param_name
        self.value = valinit
        
        valinterval = utils.construct_interval_1d(valinterval)
        valinterval = np.array(valinterval)
 
        if 'Trayectoria' in self.retrato._name_: 
            self.ax = self.retrato.sliders_fig.add_axes([0.25, 0.88 - 0.05*len(self.retrato.sliders), 0.4, 0.05])

        if 'RetratoDeFases' in self.retrato._name_:
            self.ax = self.retrato.fig.add_axes([0.25, 0.015 + 0.05*len(self.retrato.sliders), 0.4, 0.03])

        
        aux = {'valinit':valinit} if self.value else {}
        self.slider = matplot_slider(self.ax, self.param_name, *valinterval, valstep=valstep, **aux)

    def __call__(self, value):
        """
        Es la función que se hace cuando se ejecuta al objeto
        """
        try:
            self.retrato.ax.cla()
        except:
            for ax in self.retrato.ax.values():
                ax.cla()
        self.value = value
        self.retrato.plot()
