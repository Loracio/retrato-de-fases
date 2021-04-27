from retratodefases import *
from matplotlib import pyplot as plt
import numpy as np


if True:
    """
    Ejemplo 0 Círculo: una trayectoria en 2 dimensiones
    """

    def Circulo(x,y,*, w=1, z=1):
        return w*y, -z*x

    circle = Trayectoria2D(Circulo, n_points=1300, size=2, mark_start_position=True, Titulo='Just a circle')
    # Pasamos condiciones iniciales a las trayectorias:
    circle.posicion_inicial(1,1)
    circle.posicion_inicial(2,2)
    circle.add_slider('w', valinterval=[-1,5])
    circle.add_slider('z', valinterval=[-1,5])
    circle.plot()
    plt.show()

if True:
    """
    Ejemplo 1 Lorentz: dos trayectorias separadas ligeramente
    """

    def Lorentz(x,y,z,*, s=10, r=28, b=8/3):
        return -s*x+s*y, -x*z+r*x-y, x*y-b*z

    a = Trayectoria3D(Lorentz, lines=True, n_points=1300, size=3, mark_start_position=True, Titulo='Nearby IC on Lorentz attractor')
    # Pasamos condiciones iniciales a las trayectorias:
    a.posicion_inicial(10,10,10)
    a.posicion_inicial(10,10,10.0001)
    a.add_slider('r', valinterval=[24,30])
    a.plot()
    plt.show()


if True:
    """
    Ejemplo 2 Lorentz: una trayectoria coloreada en función del tiempo. Usando numba para que funcione más rápido.
    """

    def Lorentz(x,y,z,*, s=10, r=28, b=8/3):
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

    d = Trayectoria3D(Halvorsen, dF_args={'s':1.4}, n_points=10000, termalization=0, numba=True, size=2, mark_start_point=True, Titulo='Halvorsen attractor')
    d.posicion_inicial(0,5,10)
    d.plot()
    plt.show()


if True:
    """
    Ejemplo 5 Thomas: atractor con colores. Sin marcar la posición inicial
    """

    def Thomas(x,y,z,*, s=0.208186):
      return -s*x+np.sin(y), -s*y+np.sin(z), -s*z+np.sin(x)
    
    e = Trayectoria3D(Thomas, dF_args={'s':0.208186}, n_points=30000, size=1, numba=True, termalization=2000, Titulo='Thomas attractor')
    e.termaliza()
    e.plot()
    plt.show()

if True:
    """
    Ejemplo 6 Four-Wings: atractor con colores.
    """
    def Four_wings(x,y,z,*, a=0.2, b=0.01, c=-0.4):
      return a*x+y*z, b*x+c*y-x*z, -z - x*y
    
    f = Trayectoria3D(Four_wings, dF_args={'a':0.2, 'b':0.01, 'c':-0.4}, n_points=10000, runge_kutta_freq=5, size=2, termalization=2000, Titulo='Four-Wings attractor')
    f.add_slider('a', valinit=0.21, valinterval=[0.1,0.3], valstep=0.005)
    f.add_slider('b', valinit=0.01, valinterval=[0,0.3], valstep=0.005)
    f.add_slider('c', valinit=-0.4, valinterval=[-1,0], valstep=0.005)
    f.termaliza()
    f.plot()
    plt.show()

if True:
    """
    Ejemplo 7: atractor de Aizawa
    """
    def Aizawa(x,y,z,*, a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1):
        return (z-b)*x - d*y, d*x + (z-b)*y, c + a*z - z*z*z/3 - (x*x + y*y) * (1 + e*z) + f*z*x*x*x

    g = Trayectoria3D(Aizawa, dF_args={'a':0.95, 'b':0.7, 'c':0.6, 'd':3.5, 'e':0.25, 'f':0.1}, n_points=10000, size=1, termalization=2000, Titulo='Aizawa attractor')
    g.termaliza()
    g.add_slider('a', valinit=0.95, valinterval=[0,1], valstep=0.005)
    g.add_slider('b', valinit=0.7, valinterval=[0,1], valstep=0.005)
    g.add_slider('c', valinit=0.6, valinterval=[0,1], valstep=0.005)
    g.add_slider('d', valinit=3.5, valinterval=[0,4], valstep=0.05)
    g.add_slider('e', valinit=0.24, valinterval=[0,1], valstep=0.005)
    g.add_slider('f', valinit=0.1, valinterval=[0,1], valstep=0.005)
    g.plot()
    plt.show()


if True:
    """
    Ejemplo 8: atractor de Sprott
    """

    def Sprott(x, y, z, *, a=2.07, b=1.79):
        return y + a*x*y + x*z, 1 - b*x*x + y*z, x - x*x - y*y

    h = Trayectoria3D(Sprott, dF_args={'a':2.07, 'b':1.79}, n_points=10000, numba=True, size=1, termalization=2000, Titulo='Sprott attractor')
    h.termaliza()
    h.add_slider('a', valinterval=[0,5])
    h.add_slider('b', valinterval= [0,5])
    h.plot()
    plt.show()