import numpy as np
from scipy.misc import derivative
import matplotlib.pyplot as plt

class Funcion1D():
    def __init__(self, portrait, funcion, *, n_points=500, xRange=None, dF_args=None, color='g'):
        self.portrait = portrait
        self.funcion = funcion
        self.n_points = n_points
        self.color = color
        self.xRange = xRange if xRange is not None else self.portrait.Range[0,:]
        
        try:
            self.dF_args = dF_args if dF_args is not None else self.portrait.dF_args
        except:
            self.dF_args = {}
        
    def _compute_values(self):
        try:
            self.dF_args = self.portrait.dF_args
        except:
            pass
        self._x_values = np.linspace(*(self.xRange), self.n_points)
        self._y_values = self.funcion(self._x_values, **self.dF_args)
        
        
    def plot(self):
        self._compute_values()
        self.portrait.ax.plot(self._x_values, self._y_values, '-', color=self.color)
        