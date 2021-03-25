from .exceptions import *
from .utils import *
from matplotlib.widgets import Slider as matplot_slider

class Slider():
    def __init__(self, retrato, param_name, valinit=None, valstep=0.1, valinterval=[]):
        self.retrato = retrato
        self.param_name = param_name
        self.value = valinit
        
        if utils._is_number(valinterval):
            if valinterval == 0:
                raise exceptions2D.RangoInvalid('0 no es un rango válido')
            valinterval = [-valinterval,valinterval]

        elif self._is_range(valinterval):
            a,b = valinterval
            if utils._is_number(a) and utils._is_number(b):
                valinterval = [a,b]
            else:
                raise exceptions2D.RangoInvalid('el rango (1D) debe ser o un real o una lista de dos')
        else:
            raise exceptions2D.RangoInvalid(f'{valinterval} no es un rango válido')
        valinterval.sort()


        # TODO: ajustar plot. Debería ser función de la clase principal: 
        self.retrato.fig.subplots_adjust(bottom=0.25)
        self.ax = self.retrato.fig.add_axes([0.25, 0.015 + 0.05*len(self.retrato.sliders), 0.5, 0.03])
        
        aux = {'valinit':valinit} if self.value else {}
        self.slider = matplot_slider(self.ax, self.param_name, *valinterval, valstep=valstep, **aux)

    def __call__(self, value):
        """
        Es la función que se hace cuando se ejecuta al objeto
        """
        self.retrato.ax.cla()
        self.value = value
        self.retrato.plot()