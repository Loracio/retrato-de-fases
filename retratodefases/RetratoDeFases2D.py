import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from .phase_diagrams import Funcion1D, PhasePortrait


class RetratoDeFases2D(PhasePortrait):
    """
    RetratoDeFases2D
    ----------------
    Class dedicated to 2D phase diagrams.
    
    Methods
    -------    
    draw_plot : 
        Draws the streamplot. Is internaly used by method `plot`.
        
    add_funcion : 
        Adds a funcion to the `dF` plot.
    
    add_slider :
        Adds a `Slider` for the `dF` funcion.

    plot :
        Prepares the plots and computes the values. 
        Returns the axis and the figure.
    """
    _name_ = 'RetratoDeFases2D'
    def __init__(self, dF, RangoRepresentacion, *, LongitudMalla=10, dF_args={}, Densidad = 1, Polar = False, Titulo = 'Retrato de Fases', xlabel = 'X', ylabel = r"$\dot{X}$", color='rainbow'):
        """
        PhasePortrait2D
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
        ylabel : str, default='$\dot{X}$' 
            y label of the plot.
        color : str, default='rainbow'
            Matplotlib `Cmap`.
        """
        
        super().__init__(dF, RangoRepresentacion, 2, MeshDim=LongitudMalla, dF_args=dF_args, Polar=Polar, Title=Titulo, color=color)
        
        # Variables no obligatorias                                                           # Titulo para el retrato de fases.
        self.xlabel = xlabel                                                                  # Titulo en eje X
        self.ylabel = ylabel                                                                  # Titulo en eje Y

        # Variables para la representación
        self.fig, self.ax = plt.subplots()
        self.funcions = []

        # Variables que el usuario no debe emplear: son para el tratamiento interno de la clase. Es por ello que llevan el prefijo "_"
        self._X, self._Y = np.meshgrid(np.linspace(*self.Range[0,:], self.L), np.linspace(*self.Range[1,:], self.L))   #Crea una malla de tamaño L²

        if self.Polar:   
            self._R, self._Theta = (self._X**2 + self._Y**2)**0.5, np.arctan2(self._Y, self._X) # Transformacion de coordenadas cartesianas a polares

    def add_funcion(self, funcion1d, *, n_points=500, xRange=None, dF_args=None, color='g'):
        """
        Adds a funcion to the `dF` plot.
    
        Parameters
        ---------
        funcion1d : callable
            A dF type funcion.
        
        Key Arguments
        ------------
        n_points : int, default=500
            Number of points in the funcion representation.
        xRange : list, default=None
            The x range in which the points are calculated.
        dF_args : dict, default=None
            If necesary, must contain the kargs for the `dF` funcion.
        color : str, default='g' 
            String  matplotlib color identifier.
        """ 
        self.funcions.append(Funcion1D(self, funcion1d, n_points=n_points, xRange=xRange, dF_args=None, color=color))
        

    def plot(self, *, color=None):
        """
        Prepares the plots and computes the values.
        
        Returns
        -------
        tuple(matplotlib Figure, matplotlib Axis)
        
        Key Arguments
        -------------
        color : str
            Matplotlib `Cmap`.
        """
        self.draw_plot(color=color)
        self.fig.canvas.draw_idle()


    def draw_plot(self, *, color=None):
        """
        Draws the streamplot. Is internaly used by method `plot`.
        
        Returns
        -------
        matplotlib.Streamplot
        
        Key Arguments
        -------------
        color : str
            Matplotlib `Cmap`.
        """
        super().draw_plot()
        
        if self.Polar:
            self._transformacionPolares()
        else:
            self._dX, self._dY = self.dF(self._X, self._Y, **self.dF_args)
            
        colores = (self._dX**2+self._dY**2)**(0.5)
        colores_norm = matplotlib.colors.Normalize(vmin=colores.min(), vmax=colores.max())
        stream = self.ax.streamplot(self._X, self._Y, self._dX, self._dY, color=colores, cmap=color, norm=colores_norm, linewidth=1, density= self.Density)
        self.ax.set_xlim(self.Range[0,:])
        self.ax.set_ylim(self.Range[1,:])
        x0,x1 = self.ax.get_xlim()
        y0,y1 = self.ax.get_ylim()
        self.ax.set_aspect(abs(x1-x0)/abs(y1-y0))
        self.ax.set_title(f'{self.Title}')
        self.ax.set_xlabel(f'{self.xlabel}')
        self.ax.set_ylabel(f'{self.ylabel}')
        self.ax.grid()
        
        return stream
    
    
    def _transformacionPolares(self):
        """
        Devuelve la expresión del campo de velocidades en cartesianas, si la expresión del sistema viene dada en polares
        """
        self._dR, self._dTheta = self.dF(self._R, self._Theta, **self.dF_args)
        self._dX, self._dY = self._dR*np.cos(self._Theta) - self._R*np.sin(self._Theta)*self._dTheta, self._dR*np.sin(self._Theta)+self._R*np.cos(self._Theta)*self._dTheta
