from RetratoDeFases import *

"""
Ejemplo 2 con Sliders para 2 parámetros
"""

def dFPolares(r, θ, *, μ=0.5,η=0):
    return μ*r*(1 - r*r), 1+η*θ

RetratoPolares = RetratoDeFases2D(dFPolares, [-3, 3], Polar=True, Titulo='Ciclo Límite')
RetratoPolares.add_slider('μ', valinit=0.5)
RetratoPolares.add_slider('η')
RetratoPolares.plot()

"""
Ejemplo 3 con Sliders para 4 parámetros
"""

def dFLoveAffairs(R, J, *, a=1, b=0, c=-1, d=1):
    return a*J + b*R, c*R + d*J

RetratoLoveAffairs = RetratoDeFases2D(dFLoveAffairs, [-3, 3], Densidad=1.5, Titulo='Love Affairs', xlabel='R', ylabel='J')
RetratoLoveAffairs.add_slider('d', valinit=1)
RetratoLoveAffairs.add_slider('c', valinit=-1)
RetratoLoveAffairs.add_slider('b', valinit=0)
RetratoLoveAffairs.add_slider('a', valinit=1)
RetratoLoveAffairs.plot()

"""
Ejemplo 5 con Sliders para 4 parámetros: a, b, c y d
"""

def dFCentroNoLineal(x, y, *, a=1, b=1, c =1, d=1):
    return a*y-b*y**3, -c*x-d*y**2

RetratoCentroNoLineal = RetratoDeFases2D(dFCentroNoLineal, [-2,2], Densidad=2, Titulo='Centro no lineal en (0,0)', xlabel='X', ylabel='Y')
RetratoCentroNoLineal.add_slider('d')
RetratoCentroNoLineal.add_slider('c')
RetratoCentroNoLineal.add_slider('b')
RetratoCentroNoLineal.add_slider('a')
RetratoCentroNoLineal.plot()