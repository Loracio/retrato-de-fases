import numpy as np
import matplotlib.pyplot as plt

class RetratoDeFases2D:
    """
    Hace un retrato de fases de un sistema 2D.
    """
    def __init__(self, dF, RangoRepresentacion, LongitudMalla, *, Densidad = 1, Polar = False, Titulo = 'Retrato de Fases', xlabel = 'X', ylabel = 'Y'):
        """
        Inicializador de clase: inicializa las variables de la clase a los valores pasados. 
        También se definen las variables que se emplean internamente en la clase para realizar el diagrama.
        Se le debe pasar obligatoriamente una función que contenga la expresión de las derivadas de los parámetros.
        """

        # Variables obligatorias
        self.dF = dF                        # Derivadas de las variables respecto al tiempo
        self.Rango = RangoRepresentacion    # Rango de representación del diagrama
        self.L = LongitudMalla              # Número de puntos por eje para representar el diagrama (habrá L² puntos)

        # Variables no obligatorias
        self.Densidad = Densidad            # [RetratoDeFases.py](RetratoDeFases.py)
        self.Polar = Polar                  # Si se pasan las coordenadas en polares, marcar como True.
        self.Titulo = Titulo                # Titulo para el retrato de fases.
        self.xlabel = xlabel                # Titulo en eje X
        self.ylabel = ylabel                # Titulo en eje Y


        # Variables que el usuario no debe emplear: son para el tratamiento interno de la clase. Es por ello que llevan el prefijo "_"
        self._X, self._Y = np.meshgrid(np.linspace(self.Rango[0], self.Rango[1], self.L), np.linspace(self.Rango[0], self.Rango[1], self.L))   #Crea una malla de tamaño L²

        if Polar:   
            self._R, self._Theta = (self._X**2 + self._Y**2)**0.5, np.arctan2(self._Y, self._X) # Transformacion de coordenadas cartesianas a polares
            self._dR, self._dTheta = self.dF(self._R, self._Theta) # Calcula el campo de velocidades en cada uno de los puntos de la malla
            self._dX, self._dY = self._dR*np.cos(self._Theta) - self._R*np.sin(self._Theta)*self._dTheta, self._dR*np.sin(self._Theta)+self._R*np.cos(self._Theta)*self._dTheta
        else:
            self._dX, self._dY = self.dF(self._X, self._Y) # Calcula el campo de velocidades en cada uno de los puntos de la malla


    def plot(self,mode="unico",tiempo=1, label=None):
        '''Puede ser "unico" o "continuo".
        Es útil cuando se estudia una bifurcación'''
        
       #if mode=="unico":
       #    colorines = (self._dX**2+self._dY**2)**(0.5)
       #    plt.streamplot(self._X, self._Y, self._dX, self._dY, color=colorines, linewidth=1.5, density= self.Densidad)
       #    plt.axis('square')
       #    plt.axis([self.Rango[0], self.Rango[1], self.Rango[0], self.Rango[1]])
       #    plt.title(f'{self.Titulo}')
       #    plt.xlabel(f'{self.xlabel}')
       #    plt.ylabel(f'{self.ylabel}')
       #    plt.grid()
       #    plt.show()
       #if mode=="continuo":
       #    colorines = (self._dX**2+self._dY**2)**(0.5)
       #    plt.streamplot(self._X, self._Y, self._dX, self._dY, color=colorines, linewidth=1.5, density= self.Densidad)
       #    plt.pause(1)
        plt.clf()
        colorines = (self._dX**2+self._dY**2)
        plt.streamplot(self._X, self._Y, self._dX, self._dY, color=colorines, linewidth=1.5, density= self.Densidad, cmap='plasma')
        plt.axis('square')
        plt.axis([self.Rango[0], self.Rango[1], self.Rango[0], self.Rango[1]])
        if label==None:
            plt.title(f'{self.Titulo}')
        else:
            plt.title(f'{self.Titulo}, r = {label:.2f}')
        plt.xlabel(f'{self.xlabel}')
        plt.ylabel(f'{self.ylabel}')
        plt.grid()

        if mode=="unico":
            plt.show()
        
        if mode=="continuo":
            if label==None:
                plt.title(f'{self.Titulo}')
            else:
                plt.title(f'{self.Titulo}, r = {label:.2f}')
            plt.pause(tiempo)
