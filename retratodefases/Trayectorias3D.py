import random
from inspect import signature

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from . import sliders
from .exceptions import *
from .utils import utils


class Trayectoria3D:
    """
    Computa una trayectoria en un sistema 3D.
    """
    def __init__(self, dF, *, RangoRepresentacion=None, lines=False, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, **kargs):
        """
        Inicializador de clase: inicializa las variables de la clase a los valores pasados. 
        También se definen las variables que se emplean internamente en la clase para realizar el diagrama.
        Se le debe pasar obligatoriamente una función que contenga la expresión de las derivadas de los parámetros.
        """

        # Variables obligatorias
        self.dF_args = dF_args                           # Argumentos extras que haya que proporcionar a la función dF
        self.dF = dF                                     # Derivadas de las variables respecto al tiempo
        self.Rango = RangoRepresentacion                 # Rango de representación del diagrama
        self.dimension = 3

        #(Polar = False, Titulo = 'Trayectoria', xlabel = 'X', ylabel = 'Y', zlabel = 'Z', numba=False)

        self.values = []
        self.velocity = []
        self.initial_conditions = []

        try: 
            if kargs['numba']:
                import numba as _numba
                from numba import jit, vectorize
                self.dF = jit(self.dF, nopython=True, cache=True, parallel=True)
                if not dF_args:
                    exceptions.dFArgsRequired()
        except KeyError:
            pass


        # Variables Runge-Kutta
        self.h = runge_kutta_step
        self.runge_kutta_freq = runge_kutta_freq
        self.n_points = n_points
        
        # Variables no obligatorias
        self.Titulo = kargs['Titulo'] if kargs.get('Titulo') else 'Trayectoria'             # Titulo para el retrato de fases.
        self.xlabel = kargs['xlabel'] if kargs.get('xlabel') else 'X'                       # Titulo en eje X
        self.ylabel = kargs['ylabel'] if kargs.get('ylabel') else 'Y'                       # Titulo en eje Y
        self.zlabel = kargs['zlabel'] if kargs.get('zlabel') else 'Z'                       # Titulo en eje Z


        # Variables para la representación
        figX, axX= plt.subplots()
        figY, axY= plt.subplots()
        figZ, axZ= plt.subplots()
        fig3d = plt.figure()
        ax3d = fig3d.add_subplot(projection='3d')

        self.fig = {
            'X': figX,
            'Y': figY,
            'Z': figZ,
            '3d': fig3d
        }
        self.ax = {
            'X': axX,
            'Y': axY,
            'Z': axZ,
            '3d': ax3d
        }
        
        self.sliders = {}
        self.sliders_fig = False

        self.lines = lines

        self.termalization = kargs.get('termalization')
        if not self.termalization:
            self.termalization = 0
        self.size = kargs.get('size')
        if not self.size:
            self.size = 0.5
        self.color = kargs.get('color')
        self._mark_start_point = kargs.get('mark_start_point')

        # Variables que el usuario no debe emplear: son para el tratamiento interno de la clase. Es por ello que llevan el prefijo "_"
        #! elf._X, self._Y = np.meshgrid(np.linspace(*self.Rango[0,:], self.L), np.linspace(*self.Rango[1,:], self.L))   #Crea una malla de tamaño L²
        #self._XYZ = np.meshgrid(*[np.linspace(*r, l) for r, l in zip(self.Rango, self.L)])

        #! Falta arreglar esto para tres coordenadas. Me da pereza
        #if self.Polar:   
        #    self._R, self._Theta = (self._X**2 + self._Y**2)**0.5, np.arctan2(self._Y, self._X) # Transformacion de coordenadas cartesianas a polares

    def _create_sliders_plot(self):
        if not isinstance(self.sliders_fig, plt.Figure):
            self.sliders_fig, self.sliders_ax = plt.subplots() 


    def rungekutta_time_independent(self, initial_values):
        values = initial_values
        if not isinstance(values, np.ndarray):
            values = np.array(values)
        while True:
            k1 = np.array(self.dF(*(values), **self.dF_args))
            k2 = np.array(self.dF(*(values+0.5*k1*self.h), **self.dF_args))
            k3 = np.array(self.dF(*(values+0.5*k2*self.h), **self.dF_args))
            k4 = np.array(self.dF(*(values+k3*self.h), **self.dF_args))
            diff = 1/6*self.h*(k1+2*k2+2*k3+k4)
            values += diff
            yield values, diff


    def compute_trayectory(self, initial_values):
        values = np.zeros([3,self.n_points])


        #! Mejorar estas 5 líneas
        try:
            values[:,0] = np.array(initial_values)
        except:
            values[:,0] = np.array([random.random(), random.random(), random.random()])

        velocity = np.zeros([3,self.n_points])
        
        for i in range(1, self.n_points + self.termalization):
            for j in range(self.runge_kutta_freq):
                new_value = next(self.rungekutta_time_independent(values[:,0]))
            if i>=self.termalization:
                values[:,i-self.termalization], velocity[:,i-self.termalization] = new_value

        return values, velocity
        
    def estabiliza(self, *args, **kargs):
        self.posicion_inicial(*args, **kargs)

    def posicion_inicial(self, *args, **kargs):
        self.prepare_plot()
        self.initial_conditions.append(np.array(args))   
            
        self._calculate_values(*args, **kargs)
        
    def _calculate_values(self, *args, **kargs):
        values, velocity = self.compute_trayectory(args)
        self.values.append(values)
        self.velocity.append(velocity)


    def plot(self, *args, **kargs):

        if not self.lines:
            self._calculate_values(self.initial_conditions)

        cmap = kargs.get('color')

        for val, vel in zip(self.values, self.velocity):
            if self.lines:

                    self.ax['3d'].plot3D(*val[:,1:])
                    self.ax['X'].plot(val[1,1:], val[2,1:])
                    self.ax['Y'].plot(val[0,1:], val[2,1:])
                    self.ax['Z'].plot(val[0,1:], val[1,1:])
            else:
                def norma(v):
                    suma = 0
                    for i in range(3):
                        suma += v[i]**2
                    return np.sqrt(suma)
                if self.color == 't':
                    color = np.linspace(0,1, vel.shape[1])
                else:
                    cmap = self.color
                    color = norma(vel[:])
                    color /= color.max()

                self.ax['3d'].scatter3D(*val, s=self.size, c=color, cmap=cmap)
                self.ax['X'].scatter(val[1,:], val[2,:], s=self.size, c=color, cmap=cmap)
                self.ax['Y'].scatter(val[0,:], val[2,:], s=self.size, c=color, cmap=cmap)
                self.ax['Z'].scatter(val[0,:], val[1,:], s=self.size, c=color, cmap=cmap)

            if self._mark_start_point:
                self.ax['3d'].scatter3D(*val[:,0], size=self.size+1, c=[0])
                self.ax['X'].scatter(val[1,0], val[2,0], size=self.size+1, c=[0])
                self.ax['Y'].scatter(val[0,0], val[2,0], size=self.size+1, c=[0])
                self.ax['Z'].scatter(val[0,0], val[1,0], size=self.size+1, c=[0])

        for fig in self.fig.values():
            fig.canvas.draw_idle()
        try:
            self.sliders_fig.canvas.draw_idle()
        except:
            pass

    def prepare_plot(self):

        #self.dF_args = {name: slider.value for name, slider in self.sliders.items() if slider.value!= None}

        #if self.Polar:
        #    self._transformacionPolares()
        #else:
        #    #! self._dX, self._dY = self.dF(self._X, self._Y, **self.dF_args)
        #    self._dXYZ = self.dF(*self._XYZ, **self.dF_args)
        #colores = (self._XYZ[0]**2+self._XYZ[1]**2+self._XYZ[2]**2)**(0.5)
        #colores_p = self.norma()
        #colores_norm = matplotlib.colors.Normalize(vmin=colores_p.min(), vmax=colores_p.max())
        #! stream = self.ax.streamplot(self._X, self._Y, self._dX, self._dY, color=colores_p, cmap=color, norm=colores_norm, linewidth=1, density= self.Densidad)
        #stream = self.ax.quiver(*self._XYZ, *self._dXYZ, length=0.1)#, cmap='Reds')

        self.ax['3d'].set_title(f'{self.Titulo}')
        if self.Rango is not None:
            self.ax['3d'].set_xlim(self.Rango[0,:])
            self.ax['3d'].set_ylim(self.Rango[1,:])
            self.ax['3d'].set_zlim(self.Rango[2,:])
        self.ax['3d'].set_xlabel(f'{self.xlabel}')
        self.ax['3d'].set_ylabel(f'{self.ylabel}')
        self.ax['3d'].set_zlabel(f'{self.zlabel}')
        self.ax['3d'].grid()

        self.ax['X'].set_title(f'{self.Titulo}: YZ')
        if self.Rango is not None:
            self.ax['X'].set_xlim(self.Rango[1,:])
            self.ax['X'].set_ylim(self.Rango[2,:])
        self.ax['X'].set_xlabel(f'{self.ylabel}')
        self.ax['X'].set_ylabel(f'{self.zlabel}')
        self.ax['X'].grid()

        self.ax['Y'].set_title(f'{self.Titulo}: XZ')
        if self.Rango is not None:
            self.ax['Y'].set_xlim(self.Rango[0,:])
            self.ax['Y'].set_ylim(self.Rango[2,:])
        self.ax['Y'].set_xlabel(f'{self.xlabel}')
        self.ax['Y'].set_ylabel(f'{self.zlabel}')
        self.ax['Y'].grid()

        self.ax['Z'].set_title(f'{self.Titulo}: XY')
        if self.Rango is not None:
            self.ax['Z'].set_xlim(self.Rango[0,:])
            self.ax['Z'].set_ylim(self.Rango[1,:])
        self.ax['Z'].set_xlabel(f'{self.xlabel}')
        self.ax['Z'].set_ylabel(f'{self.ylabel}')
        self.ax['Z'].grid()


    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Añade un slider sobre un plot ya existente.
        """
        self._create_sliders_plot()
        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])
    
    
    def _transformacionPolares(self):
        """
        Devuelve la expresión del campo de velocidades en cartesianas, si la expresión del sistema viene dada en polares
        """
        self._dR, self._dTheta = self.dF(self._R, self._Theta, **self.dF_args)
        self._dX, self._dY = self._dR*np.cos(self._Theta) - self._R*np.sin(self._Theta)*self._dTheta, self._dR*np.sin(self._Theta)+self._R*np.cos(self._Theta)*self._dTheta



    # Funciones para asegurarse que los parametros introducidos son válidos
    @property
    def dF(self):
        return self._dF

    @dF.setter
    def dF(self, func):
        if not callable(func):
            raise exceptions.dFNotCallable(func)
        try:
            sig = signature(func)
        except ValueError:
            pass
        else:
            if len(sig.parameters)<3 + len(self.dF_args):
                raise exceptions.dFInvalid(sig, self.dF_args)
        self._dF = func

    @property
    def Rango(self):
        return self._Rango

    @Rango.setter
    def Rango(self, value):
        if value == None:
            self._Rango = None
            return
        self._Rango = np.array(utils.construct_interval(value, dim=3))


    @property
    def L(self):
        return self._L

    @L.setter
    def L(self, value):
        self._L=value
        if utils.is_number(value):
            self._L = [value for _ in range(self.dimension)]
        while len(self._L)<self.dimension:
            self._L.append(10)


    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise exceptions.dF_argsInvalid(value)
        self._dF_args = value
