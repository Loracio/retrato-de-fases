import matplotlib.pyplot as plt
import numpy as np

from .phase_diagrams import PhasePortrait
from .utils import utils


class RetratoDeFases3D(PhasePortrait):
    """
    RetratoDeFases3D
    ----------------
    Class dedicated to 3D phase diagrams.
    
    Methods
    -------    
    norma : 
        Must convert position and velocity to float representing colour.
        
    draw_plot : 
        Draws the streamplot. Is internaly used by method `plot`.
    
    add_slider :
        Adds a `Slider` for the `dF` funcion.

    plot :
        Prepares the plots and computes the values. 
        Returns the axis and the figure.
    """
    _name_ = 'RetratoDeFases3D'
    
    def __init__(self, dF, RangoRepresentacion, *, LongitudMalla=10, dF_args={}, Polar = False, Titulo = 'Retrato de Fases', xlabel = 'X', ylabel = 'Y', zlabel = 'Z', color='rainbow'):
        """
        PhasePortrait3D
        ---------------
        
        Parameters
        ----------
        dF : callable
            A dF type funcion.
        RangoRepresentacion : [x_range, y_range]
            Ranges of the axis in the main plot.
            
        Key Arguments
        -------------
        LongitudMalla : int, default=10
            Number of elements in the arrows grid.
        dF_args : dict
            If necesary, must contain the kargs for the `dF` funcion.
        Densidad : float, default=1
            Number of elements in the arrows grid plot.
        Polar : bool, default=False
            Whether to use polar coordinates or not.
        Titulo : str, default='Titulo' 
        xlabel : str, default='X'
            x label of the plot.
        ylabel : str, default='Y' 
            y label of the plot.
        zlabel : str, default='Z' 
            z label of the plot.
        color : str, default='rainbow'
            Matplotlib `Cmap`.
        """
        super().__init__(dF, RangoRepresentacion, 3, MeshDim=LongitudMalla, dF_args=dF_args, Polar=Polar, Title=Titulo, color=color)
        
        # Variables no obligatorias                                                               # Titulo para el retrato de fases.
        self.xlabel = xlabel                                                                  # Titulo en eje X
        self.ylabel = ylabel                                                                  # Titulo en eje Y
        self.zlabel = zlabel                                                                  # Titulo en eje Z

        # Variables para la representación
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')

        # Variables que el usuario no debe emplear: son para el tratamiento interno de la clase. Es por ello que llevan el prefijo "_"
        self._XYZ = np.meshgrid(*[np.linspace(*r, l) for r, l in zip(self.Rango, self.L)])
        self._dXYZ = []*3

        # TODO: wtf?
        #* Teóricamente, debería estar arreglado, pero repito, teóricamente. Bueno, es incorrecto por lo que explico en los comentarios de las líneas anteriores, pero sería meterle las componentes de la lista
        if self.Polar:   
            self._R, self._Theta, self._Phi = (self._XYZ[0]**2 + self._XYZ[1]**2 + self._XYZ[2]**2)**0.5, np.arctan2(self._XYZ[1], self._XYZ[0]), np.arctan2(((self._XYZ[0]**2 + self._XYZ[1]**2)**0.5), self._XYZ[2])  # Transformacion de coordenadas cartesianas a esféricas


    def norma(self):
        """
        Converts position and velocity to float color indicator.
        
        Example
        -------
        ```
        def norma(self):
            result = np.zeros(self.L)
            for i in self._XYZ:
                result += i*i
            return np.sqrt(result)
        ```
        """
        
        result = np.zeros(self.L)
        for i in self._XYZ:
            result += i*i
        return np.sqrt(result)


    def draw_plot(self, *, color=None):
        """
        Draws the streamplot. Is internaly used by method `plot`.
        
        Returns
        -------
        matplotlib.StreamplotSet
        
        Key Arguments
        -------------
        color : str
            Matplotlib `Cmap`.
        """
        if self.Polar:
            self._transformacionEsfericas()
        else:
            self._dXYZ = self.dF(*self._XYZ, **self.dF_args)
        stream = self.ax.quiver(*self._XYZ, *self._dXYZ, length=0.01)
        self.ax.set_title(f'{self.Titulo}')
        self.ax.set_xlabel(f'{self.xlabel}')
        self.ax.set_ylabel(f'{self.ylabel}')
        self.ax.set_zlabel(f'{self.zlabel}')
        self.ax.grid()
        
        return stream

    
    def _transformacionEsfericas(self):
        """
        Devuelve la expresión del campo de velocidades en cartesianas, si la expresión del sistema viene dada en esféricas
        """
        self._dR, self._dTheta, self._dPhi = self.dF(self._R, self._Theta, self._Phi **self.dF_args)
        self._dXYZ[0], self._dXYZ[1], self._dXYZ[2] = self._dR*np.cos(self._Theta)*np.sin(self._Phi) - self._R*np.sin(self._Theta)*self._dTheta*np.sin(self._Phi) + self._R*np.sin(self._Theta)*np.cos(self._Phi)*self._dPhi, self._dR*np.sin(self._Theta)*np.sin(self._Phi) + self._R*np.cos(self._Theta)*self._dTheta*np.sin(self._Phi) + self._R*np.sin(self._Theta)*np.cos(self._Phi)*self._dPhi, self._dR*np.cos(self._Phi) - self._R*np.sin(self._Phi)*self._dPhi


    # Funciones para asegurarse que los parametros introducidos son válidos
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
