from matplotlib import pyplot as plt
import numpy as np
from .maps import Map
import matplotlib
#from multiprocessing as mp
#import concurrent

class Map1D:
    _name_ = 'Map1D'
    def __init__(self, dF, x_range, y_range, n_points, *, dF_args, Titulo='Mapa 1D', xlabel=r'control parameter', ylabel=r'$X_{n+1}$', **kargs):
        # Variables obligatorias
        # Argumentos extras que haya que proporcionar a la función dF
        self.dF_args = dF_args
        # Derivadas de las variables respecto al tiempo
        self.dF = dF
        # Rango de representación del diagrama
        self.Rango = x_range, y_range
        # Números de puntos en el que se calculará cada trayectoria
        self.n_points = n_points
        self.dimension = 1

        # Variables no obligatorias
        # Titulo para el retrato de fases.
        self.Titulo = Titulo
        # Titulo en eje X
        self.xlabel = xlabel
        # Titulo en eje Y
        self.ylabel = ylabel

        # TODO: esto con numba va a volar
        try:
            if kargs['numba']:
                from numba import jit
                jit(self._compute_data)
        except:
            pass
        
        # Variables para la representación
        self.fig, self.ax = plt.subplots()
        self.color = kargs.get('color')
        if not self.color:
            self.color = 'rainbow'

        self.maps = {}
        #! No se si podríamos implementar sliders aquí, no creo que sea útil
        self.sliders = {}


        self.size = kargs.get('size')
        if self.size is None:
            self.size = 1
        self.thermalization = kargs.get('thermalization')


    def _compute_data(self, initial_value, param_name, param_interval, param_delta, *, limit_cicle_check=50, delta=0.0001):

        self._range = np.arange(param_interval[0], param_interval[1]+ param_delta, param_delta)

        for i, param in enumerate(self._range):
            self.dF_args.update({param_name: param})

            self.maps.update({param: Map.instance_and_compute_all(self, self.dF, self.dimension,
                             self.n_points, self.dF_args, initial_value, thermalization=self.thermalization,
                             limit_cicle_check=50, delta=delta)})
            
       #self._range = np.arange(param_interval[0], param_interval[1]+ param_delta, param_delta)

       #data = []
       #iterable= []
       #dF_args = self.dF_args.copy()
       
       #self.maps = [Map(self, self.dF, self.dimension, self.n_points, self.dF_args, initial_value, thermalization=self.thermalization, limit_cicle_check=50)]
       
       #for i, param in enumerate(self._range):
       #    dF_args.update({param_name: param})
       #    iterable.append((self, self.dF, self.dimension, self.n_points, dF_args, initial_value, 
       #                {'thermalization':self.thermalization, 'limit_cicle_check':50}))
       #    
       #    
       #with concurrent.futures.ProcessPoolExecutor() as executor:
       #    data = executor.map(Map.instance_and_compute_all, iterable)

       #    for dat, param in zip(data, self._range):
       #        self.maps.update(
       #            {param: dat}
       #            )



    def _prepare_plot(self):
        self.ax.set_title(f'{self.Titulo}')
        self.ax.set_xlim(*self.Rango[0])
        self.ax.set_ylim(*self.Rango[1])
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.grid()


    def plot(self, *, color=None):
        self._prepare_plot()
        
        if color is not None:
            self.color = color
            
        cmap = self.color
        colores_norm = plt.Normalize(vmin=self.Rango[1][0], vmax=self.Rango[1][1])
        for i in self._range:
            values = self.maps[i].positions
            color=values[0,0:-2]
            range_x = np.zeros(len(color)) + i
            self.ax.scatter(
                range_x, values[0,1:-1],
                s=self.size, c=color, cmap=cmap, norm=colores_norm
            )
            
        self.fig.colorbar(matplotlib.cm.ScalarMappable(norm=colores_norm, cmap=cmap))
        self.fig.colorbar.ax.set_ylabel(r'$X_{n}$', rotate=270)