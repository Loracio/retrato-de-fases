from retratodefases import Map1D
from matplotlib import pyplot as plt

def Logistic(x, *, r=1.5):
    return r*x*(1-x)

a = Map1D(Logistic, [0,3.9], [0,1], 500, thermalization=50, size=2)
a.plot_over_variable('r', [0,3.9], 0.05)
f, ax = a.plot_trajectory(200, dF_args={'r':3.8}, color='black')
a.add_funcion(Logistic, n_points=50, dF_args={'r':3.2})
a.plot()
plt.show()