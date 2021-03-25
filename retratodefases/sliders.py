from exceptions import *

class Slider():
    def __init__(self, retrato, param_name):
        self.retrato = retrato
        self.param_name = param_name
        
        if self._is_number(valinterval):
            if valinterval == 0:
                raise RangoInvalid('0 no es un rango válido')
            valinterval = [-valinterval,valinterval]

        elif self._is_range(valinterval):
            a,b = valinterval
            if self._is_number(a) and self._is_number(b):
                valinterval = [a,b]
            else:
                raise RangoInvalid('el rango (1D) debe ser o un real o una lista de dos')
        else:
            raise RangoInvalid(f'{valinterval} no es un rango válido')
        valinterval.sort()


        # TODO: ajustar plot. Debería ser función de la clase principal: 
        self.retrato.fig.subplots_adjust(bottom=0.25)
        self.sbox = self.retrato.get_position()
        self.ax = self.fig.add_axes([0.25, 0.015 + 0.05*len(self._sliders), 0.5, 0.03])
        
        aux = {'valinit':valinit} if valinit else {}
        self.slider = Slider(ax_Parametro, param_name, *valinterval, valstep=valstep, **aux)
    
    def __call__(self, value):
        self.retrato.ax.cla()
        self.retrato._sliders[self.param_name]['value'] = value
        self.retrato.dibuja_streamplot(color=self.retrato.color)
        self.retrato.fig.canvas.draw_idle()
