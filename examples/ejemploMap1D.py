from retratodefases import Map1D
from retratodefases import Cobweb
from matplotlib import pyplot as plt

def Logistic(x, *, r=1.5):
    return r*x*(1-x)

def line(x, *, r=1.5):
    return 1.5*r/x

# Create an instance of Map1D
Logistic_Map = Map1D(Logistic, [2,3.9], [0,1], 500, thermalization=50, size=2)


# We want to plot for r in the range 2.05 < r < 3.85. Every 0.005.
Logistic_Map.plot_over_variable('r', [2.05,3.85], 0.005)

# We also want to plot a single trajectory with r = 3.8.
f, ax = Logistic_Map.plot_trajectory(200, dF_args={'r':3.8}, color='black')

# We add a non interesting funcion r + x to the plot, because it is an example.
Logistic_Map.add_funcion(line, n_points=50, xRange=[2.2,3.8], dF_args={'r':3.2}, color='green')

# Plot everything said before. 
f, ax = Logistic_Map.plot()

# Disable the grid, because again, example.
ax.grid()

# Cobweb plot and time series.
LogisticCobweb = Cobweb(Logistic, 0.2, [0,1], dF_args={'r':1.5}, yrange=[0,1])
LogisticCobweb.add_slider('r', valinit=1.5, valinterval=[0,4])
LogisticCobweb.initial_position_slider(valstep=0.01)
LogisticCobweb.plot()

# Show the plots.
plt.show()
