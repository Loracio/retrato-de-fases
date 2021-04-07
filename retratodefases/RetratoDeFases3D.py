from inspect import signature

from .exceptions import *
from . import sliders
from .utils import utils

import matplotlib
import matplotlib.pyplot as plt

import numpy as np

class RetratoDeFases3D:
    """
    Hace un retrato de fases de un sistema 3D.
    """
    #! No tiene sentido tener de keywarg la Densidad aquí, no? Me parece que streamplot solo es algo que nos salvó para 2D, igualmente el mapa de colores creo que sobra
    def __init__(self, dF, RangoRepresentacion, *, LongitudMalla=10, dF_args={}, Densidad = 1, Polar = False, Titulo = 'Retrato de Fases', xlabel = 'X', ylabel = 'Y', zlabel = 'Z', color='rainbow'):
        """
        Inicializador de clase: inicializa las variables de la clase a los valores pasados. 
        También se definen las variables que se emplean internamente en la clase para realizar el diagrama.
        Se le debe pasar obligatoriamente una función que contenga la expresión de las derivadas de los parámetros.
        """

        # Variables obligatorias
        self.dF_args = dF_args                           # Argumentos extras que haya que proporcionar a la función dF
        self.dF = dF                                     # Derivadas de las variables respecto al tiempo
        self.Rango = RangoRepresentacion                 # Rango de representación del diagrama
        self.dimension = 3                               # Dimensión en la que estamos trabajando
        
        # Variables no obligatorias
        #! Revisar la manera en que está construida la LongitudMalla, para que sirva para cualquier rango de representación
        self.L = LongitudMalla # *(self.Rango[0,0]-self.Rango[0,1])                           # Número de puntos por eje para representar el diagrama (habrá L² puntos)
        self.Densidad = Densidad                                                              # Controla la cercanía de las líneas de flujo
        self.Polar = Polar                                                                    # Si se pasan las coordenadas en polares, marcar como True.
        self.Titulo = Titulo                                                                  # Titulo para el retrato de fases.
        self.xlabel = xlabel                                                                  # Titulo en eje X
        self.ylabel = ylabel                                                                  # Titulo en eje Y
        self.zlabel = zlabel                                                                  # Titulo en eje Z


        # Variables para la representación
        #self.fig, self.ax = plt.subplots()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.color = color
        self.sliders = {}

        # Variables que el usuario no debe emplear: son para el tratamiento interno de la clase. Es por ello que llevan el prefijo "_"
        #! self._X, self._Y = np.meshgrid(np.linspace(*self.Rango[0,:], self.L), np.linspace(*self.Rango[1,:], self.L))   #Crea una malla de tamaño L²
        #? Creo que lo que se hace aquí es un iterador que mete en self._XYZ una lista de meshgrids no? Pero no veo bien por qué metes en el for a self.L, ya que solo tiene un valor, no?
        #! Le veo un poco matar moscas a cañonazos, ya que no son tantas variables como para hacerlo tan general. Porque por ejemplo para hacer el cambio de coordenadas esféricas me es más cómodo pensar en esto como tres ''arrays'' separados, self._X, self._Y, self.Z; pero bueno, supongo que simplemente es meterle las componentes de la lista
        self._XYZ = np.meshgrid(*[np.linspace(*r, l) for r, l in zip(self.Rango, self.L)])

        #* Teóricamente, debería estar arreglado, pero repito, teóricamente. Bueno, es incorrecto por lo que explico en los comentarios de las líneas anteriores, pero sería meterle las componentes de la lista
        if self.Polar:   
            self._R, self._Theta, self._Phi = (self._X**2 + self._Y**2 + self._Z**2)**0.5, np.arctan2(self._Y, self._X), np.arctan2(((self._X**2 + self._Y**2)**0.5)/(self._Z))  # Transformacion de coordenadas cartesianas a esféricas


    def plot(self, *, color=None):
        self.dibuja_streamplot(color=color if color else self.color)

        #self.ax.scatter(*self._XYZ, color='0.5')
        #self.fig.canvas.draw_idle()


    def norma(self):
        cuadrado = lambda x: x*x
        result = np.zeros(self.L)
        for i in self._XYZ:
            result += i**2
        return result**0.5


    def dibuja_streamplot(self, *, color=None):

        self.dF_args = {name: slider.value for name, slider in self.sliders.items() if slider.value!= None}

        if self.Polar:
            self._transformacionEsfericas()
        else:
            #! self._dX, self._dY = self.dF(self._X, self._Y, **self.dF_args)
            self._dXYZ = self.dF(*self._XYZ, **self.dF_args)
        colores = (self._XYZ[0]**2+self._XYZ[1]**2+self._XYZ[2]**2)**(0.5)
        colores_p = self.norma()
        colores_norm = matplotlib.colors.Normalize(vmin=colores_p.min(), vmax=colores_p.max())
        #! stream = self.ax.streamplot(self._X, self._Y, self._dX, self._dY, color=colores_p, cmap=color, norm=colores_norm, linewidth=1, density= self.Densidad)
        stream = self.ax.quiver(*self._XYZ, *self._dXYZ, length=0.1)#, cmap='Reds')
        #* Las siguientes líneas son para que el plot saliera 'proporcionado' en 2D, no he hecho plots 3D en mi vida, así que habrá que ver cómo se hace
        #self.ax.set_xlim(self.Rango[0,:])
        #self.ax.set_ylim(self.Rango[1,:])
        #x0,x1 = self.ax.get_xlim()
        #y0,y1 = self.ax.get_ylim()
        #self.ax.set_aspect(abs(x1-x0)/abs(y1-y0))
        self.ax.set_title(f'{self.Titulo}')
        self.ax.set_xlabel(f'{self.xlabel}')
        self.ax.set_ylabel(f'{self.ylabel}')
        self.ax.set_zlabel(f'{self.zlabel}')
        self.ax.grid() #? ¿Es válido en 3D?
        
        return stream


    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Añade un slider sobre un plot ya existente.
        """
        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.fig.subplots_adjust(bottom=0.25)

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])
    
    
    def _transformacionEsfericas(self):
        """
        Devuelve la expresión del campo de velocidades en cartesianas, si la expresión del sistema viene dada en esféricas
        """
        self._dR, self._dTheta, self._dPhi = self.dF(self._R, self._Theta, self._Phi **self.dF_args)
        self._dX, self._dY, self._dZ = self._dR*np.cos(self._Theta)*np.sin(self._Phi) - self._R*np.sin(self._Theta)*self._dTheta*np.sin(self._Phi) + self._R*np.sin(self._Theta)*np.cos(self._Phi)*self._dPhi, self._dR*np.sin(self._Theta)*np.sin(self._Phi) + self._R*np.cos(self._Theta)*self._dTheta*np.sin(self._Phi) + self._R*np.sin(self._Theta)*np.cos(self._Phi)*self._dPhi, self._dR*np.cos(self._Phi) - self._R*np.sin(self._Phi)*self._dPhi



    # Funciones para asegurarse que los parametros introducidos son válidos
    @property
    def dF(self):
        return self._dF

    @dF.setter
    def dF(self, func):
        if not callable(func):
            raise exceptions.dFNotCallable(func)
        sig = signature(func)
        if len(sig.parameters)<3 + len(self.dF_args):
            raise exceptions.dFInvalid(sig, self.dF_args)
        self._dF = func

    @property
    def Rango(self):
        return self._Rango

    @Rango.setter
    def Rango(self, value):
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
            self._L.append(3)


    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise exceptions.dF_argsInvalid(value)
        self._dF_args = value