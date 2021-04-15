from retratodefases import *
import matplotlib.pyplot as plt

"""
Ejemplo 1 Lorentz: dos trayectorias separadas ligeramente
"""

def Lorentz(x,y,z,*, s=10, r=28, b=8/3):
    return -s*x+s*y, -x*z+r*x-y, x*y-b*z

a = Trayectoria3D(Lorentz, lines=False, n_points=1300, color='t', size=3, mark_start_position=True)
# Pasamos condiciones iniciales a las trayectorias:
a.posicion_inicial(10,10,10, color='cool')
a.posicion_inicial(10,10,10.0001, color='copper')
plt.show()



"""
Ejemplo 2 Lorentz: atractor con colores (sin lineas). Usando numba para que funcione más rápido
"""

def Lorentz(x,y,z,*, s=10, r=28, b=8/3):
    return -s*x+s*y, -x*z+r*x-y, x*y-b*z

b = Trayectoria3D(Lorentz, dF_args={'s':10, 'r':28, 'b':8/3}, n_points=4000, numba=True, color='t', size=2)
b.estabiliza()
plt.show()


"""
Ejemplo 3 Rossler: atractor con colores.
"""

def Rossler(x,y,z,*, s, r, b):
    return -(y+z), s*y+x, b+z*(x-r)

b = Trayectoria3D(Rossler, RangoRepresentacion=[20, 20,[0,40]], dF_args={'s':0.2, 'r':5.7, 'b':0.2}, n_points=30000, numba=True, termalization=2000, size=4)
b.add_slider('r', valinit=5.7, valinterval=[0,10])
b.estabiliza()
plt.show()

