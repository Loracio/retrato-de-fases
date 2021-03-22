import RetratoDeFases as ph
import numpy as np

a = 1
b = 1
c = 1

def dF(x, y):
    _X = a*x+x**3-x**5
    _Y = b+c*x**2
    return _X, _Y

for i in np.linspace(-0.5,0.5,20):
    a=i
    Retrato = ph.RetratoDeFases2D(dF,RangoRepresentacion = [-2,2], LongitudMalla = 80, Polar=True)
    Retrato.plot(mode="continuo",tiempo=0.2,label=a)
