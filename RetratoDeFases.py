from inspect import signature

import matplotlib.pyplot as plt
import numpy as np


class RetratoExceptions(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class dFNotCallable(RetratoExceptions):
    def __init__(self, func):
        super().__init__(f"El objeto {func} no es una función")

class dFInvalid(RetratoExceptions):
    def __init__(self, sig, dF_args):
        super().__init__(f"La funcion `dF` tiene {len(sig.parameters)} argumentos, se han pasado {2+len(dF_args)}")

class dF_argsInvalid(RetratoExceptions):
    def __init__(self, dF_args):
        super().__init__(f"El objeto `dF_args={dF_args}` debe ser un diccionario, no {type(dF_args)}")


class RetratoDeFases2D:
    """
    Hace un retrato de fases de un sistema 2D.
    """
    def __init__(self, dF, RangoRepresentacion, *, LongitudMalla=10, dF_args={}, Densidad = 1, Polar = False, Titulo = 'Retrato de Fases', xlabel = 'X', ylabel = r"$\dot{X}$"):
        """
        Inicializador de clase: inicializa las variables de la clase a los valores pasados. 
        También se definen las variables que se emplean internamente en la clase para realizar el diagrama.
        Se le debe pasar obligatoriamente una función que contenga la expresión de las derivadas de los parámetros.
        """

        # Variables obligatorias
        self.dF_args = dF_args                           # Argumentos extras que haya que proporcionar a la función dF
        self.dF = dF                                     # Derivadas de las variables respecto al tiempo
        self.Rango = RangoRepresentacion                 # Rango de representación del diagrama
        
        # Variables no obligatorias
        self.L = int (LongitudMalla*abs(RangoRepresentacion[1]-RangoRepresentacion[0]))       # Número de puntos por eje para representar el diagrama (habrá L² puntos)
        self.Densidad = Densidad                                                              # Controla la cercanía de las líneas de flujo
        self.Polar = Polar                                                                    # Si se pasan las coordenadas en polares, marcar como True.
        self.Titulo = Titulo                                                                  # Titulo para el retrato de fases.
        self.xlabel = xlabel                                                                  # Titulo en eje X
        self.ylabel = ylabel                                                                  # Titulo en eje Y


        # Variables que el usuario no debe emplear: son para el tratamiento interno de la clase. Es por ello que llevan el prefijo "_"
        self._X, self._Y = np.meshgrid(np.linspace(self.Rango[0], self.Rango[1], self.L), np.linspace(self.Rango[0], self.Rango[1], self.L))   #Crea una malla de tamaño L²

        if self.Polar:   
            self._R, self._Theta = (self._X**2 + self._Y**2)**0.5, np.arctan2(self._Y, self._X) # Transformacion de coordenadas cartesianas a polares
            self._dR, self._dTheta = self.dF(self._R, self._Theta, *self.dF_args) # Calcula el campo de velocidades en cada uno de los puntos de la malla
            self._dX, self._dY = self._dR*np.cos(self._Theta) - self._R*np.sin(self._Theta)*self._dTheta, self._dR*np.sin(self._Theta)+self._R*np.cos(self._Theta)*self._dTheta
        else:
            self._dX, self._dY = self.dF(self._X, self._Y, **self.dF_args) # Calcula el campo de velocidades en cada uno de los puntos de la malla


    def plot(self, *, color=None, linewidth=1):
        colorines = (self._dX**2+self._dY**2)**(0.5)
        plt.streamplot(self._X, self._Y, self._dX, self._dY, color=colorines, linewidth=1, density= self.Densidad)
        plt.axis('square')
        plt.axis([self.Rango[0], self.Rango[1], self.Rango[0], self.Rango[1],])
        plt.title(f'{self.Titulo}')
        plt.xlabel(f'{self.xlabel}')
        plt.ylabel(f'{self.ylabel}')
        plt.grid()
        plt.show()


    # Funciones para asegurarse que los parametros introducidos son válidos
    @property
    def dF(self):
        return self._dF

    @dF.setter
    def dF(self, func):
        if not callable(func):
            raise dFNotCallable(func)
        sig = signature(func)
        if len(sig.parameters)<2 + len(self.dF_args):
            raise dFInvalid(sig, self.dF_args)
        self._dF = func

    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise dF_argsInvalid(value)
        self._dF_args = value