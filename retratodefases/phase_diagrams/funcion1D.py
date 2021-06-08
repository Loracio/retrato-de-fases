import numpy as np
from scipy.misc import derivative
import matplotlib.pyplot as plt

class Funcion1D():
    """
    Funcion1D
    --------
    Class dedicated to 1 dimension funcions `y = f(x)`. 
    Useful where it is necessary to plot a funcion over a plot.
    
    Integrated via method `add_funcion` in:
        -Map1D
        
        -Cobweb
        
        -PhasePortrait2D 
    
    Methods
    -------
    compute_values :
        Computes the values.
        Returns : `self._x_values, self._y_values`
        
    plot : 
        Computes the values and plots them.
        Returns : `plt.axis`
    """
    
    def __init__(self, portrait, funcion, *, n_points=500, xRange=None, dF_args=None, color='g'):
        """
        Funcion1D
        --------
        Parameters
        ----------
        portrait : 
            Class that uses the Funcion1D.
        Range : [x_range, y_range]
            Ranges of the axis in the main plot.
        n_points : int
            Maximum number of points
        """
        self.portrait = portrait
        self.funcion = funcion
        self.n_points = n_points
        self.color = color
        self.xRange = xRange if xRange is not None else self.portrait.Range[0,:]
        
        try:
            self.dF_args = dF_args if dF_args is not None else self.portrait.dF_args
        except:
            self.dF_args = {}
        
    def compute_values(self):
        """
        Computes the values.
        
        Returns
        -------
        tuple
            `self._x_values, self._y_values`
        """
        self._x_values = np.linspace(*(self.xRange), self.n_points)
        self._y_values = self.funcion(self._x_values, **self.dF_args)
        
        return self._x_values, self._y_values
        
        
    def plot(self, *, axis=None, style='-'):
        """
        Computes the values and plots them.
        
        Returns
        ------- 
        matplotlib.Axis
        
        Key Arguments
        -----
        axis : matplotlib.Axis
            Required if you want to plot the funcion in a specific Axis. By default it takes the axis of the portrait.
        style : str
            A format strings for the curve style. Must be passed as a Key Argument
        """
        if axis is None:
            axis = self.portrait.ax
        
        self.compute_values()
        self.portrait.ax.plot(self._x_values, self._y_values, style, color=self.color)
        
        return axis