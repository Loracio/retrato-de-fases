from retratodefases import *
import matplotlib.pyplot as plt

"""
Ejemplo 1 Lorentz: dos trayectorias separadas ligeramente
"""

def Lorentz(x,y,z,*, s=10, r=28, b=8/3):
    return -s*x+s*y, -x*z+r*x-y, x*y-b*z

a = Trayectoria3D(Lorentz, dF_args={'s':10, 'r':28, 'b':8/3}, lines=True, n_points=2000)
# Pasamos condiciones iniciales a las trayectorias:
a.posicion_inicial(10,10,10)
a.posicion_inicial(10,10,10.0001)
plt.show()



"""
Ejemplo 2 Lorentz: atractor con colores (sin lineas). Usando numba para que funcione más rápido
"""

def Lorentz(x,y,z,*, s=10, r=28, b=8/3):
    return -s*x+s*y, -x*z+r*x-y, x*y-b*z

b = Trayectoria3D(Lorentz, dF_args={'s':10, 'r':28, 'b':8/3}, n_points=40000, numba=True)
b.estabiliza()
plt.show()