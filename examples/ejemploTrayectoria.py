from retratodefases import *
from matplotlib import pyplot as plt
import numpy as np

if True:
    """
    Ejemplo 1 Lorentz: dos trayectorias separadas ligeramente
    """

    def Lorentz(x,y,z,*, s=10, r=28, b=8/3):
        return -s*x+s*y, -x*z+r*x-y, x*y-b*z

    a = Trayectoria3D(Lorentz, lines=True, n_points=1300, size=3, mark_start_position=True, Titulo='Lorentz trayectory')
    # Pasamos condiciones iniciales a las trayectorias:
    a.posicion_inicial(10,10,10)
    a.posicion_inicial(10,10,10.0001)
    a.add_slider('r', valinterval=[24,30])
    a.plot()
    plt.show()


if True:
    """
    Ejemplo 2 Lorentz: una trayectoria coloreada en función del tiempo. Usando numba para que funcione más rápido
    """

    def Lorentz(x,y,z,*, s, r, b):
        return -s*x+s*y, -x*z+r*x-y, x*y-b*z

    b = Trayectoria3D(Lorentz, dF_args={'s':10, 'r':28, 'b':8/3}, n_points=4000, numba=True, color='t', size=2, Titulo='Lorentz attractor')
    b.posicion_inicial(10,10,10)
    b.plot()
    plt.show()



if True:
    """
    Ejemplo 3 Rossler: atractor con colores.
    """
    
    def Rossler(x,y,z,*, s=10, r=28, b=8/3):
        return -(y+z), s*y+x, b+z*(x-r)
    
    c = Trayectoria3D(Rossler, RangoRepresentacion=[20, 20,[0,40]], dF_args={'s':0.2, 'r':5.7, 'b':0.2}, n_points=20000, numba=True, termalization=2000, size=4, Titulo= 'Rossler attractor')
    c.add_slider('r', valinit=5.7, valinterval=[0,10])
    c.termaliza()
    c.plot()
    plt.show()

if True:
    """
    Ejemplo 4 Halvorsen: atractor con colores. Marcando la posición inicial
    """

    def Halvorsen(x,y,z, *, s=1.4):
        delta = (3*s+15)
        return -s*x+2*y-4*z-y**2+delta , -s*y+2*z-4*x-z**2+delta, -s*z+2*x-4*y-x**2+delta

    a = Trayectoria3D(Halvorsen, dF_args={'s':1.4}, n_points=10000, termalization=0, numba=True, size=2, mark_start_point=True, Titulo='Halvorsen attractor')
    a.posicion_inicial(0,5,10)
    a.plot()
    plt.show()


if True:
    """
    Ejemplo 5 Thomas: atractor con colores. Sin marcar la posición inicial
    """

    def Thomas(x,y,z,*, s=0.208186):
      return -s*x+np.sin(y), -s*y+np.sin(z), -s*z+np.sin(x)
    
    d = Trayectoria3D(Thomas, dF_args={'s':0.208186}, n_points=30000, size=1, numba=True, termalization=2000, Titulo='Thomas attractor')
    d.termaliza()
    d.plot()
    plt.show()

if True:
    """
    Ejemplo 6 Four-Wings: atractor con colores.
    """
    def Four_wings(x,y,z,*, a=0.2, b=0.01, c=-0.4):
      return a*x+y*z, b*x+c*y-x*z, -z - x*y
    
    e = Trayectoria3D(Four_wings, n_points=10000, runge_kutta_freq=5, size=2, termalization=2000, Titulo='Four-Wings attractor')
    e.add_slider('a', valinit=0.21, valinterval=[0.1,0.3], valstep=0.005)
    e.termaliza()
    e.plot()
    plt.show()