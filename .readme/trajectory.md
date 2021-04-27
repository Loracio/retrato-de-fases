
# trajectory
> *class* retratodefases.trajectories.**trajectory**(*dF, dimension, \*, RangoRepresentacion=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, \*\*kargs*)

Clase base de las trayectorias, permite representar trayectorias dada una función [dF](../README.md) con N parámetros obligatorios.

Las clases que hereden de ella deberán tener los siguientes métodos:

>   def _prepare_plot(self): ...

Debe preparar los gráficos: poner los títulos de ejes, de gráfica, etc.

    
>   def _plot_lines(self, val, val_init): ...

Debe dibujar en los gráficos una línea de puntos dada por la tupla de posiciones `val` y la posición inicial `val_init`, ambos de N dimensiones.


>   def _scatter_start_point(self, val_init): ...

Debe marcar la posición `val_init` de N dimensiones en los gráficos creados.

    
>   def _scatter_trajectory(self, val, color, cmap): ...

Debe marcar con puntos `val` con el color `color` y el mapa de colores `cmap`. Todos en N dimenisones.

# Ejemplo 2D:
```py
def _plot_lines(self, val, val_init):
        self.ax['Z'].plot(val[0,1:], val[1,1:], label=f"({','.join(tuple(map(str, val_init)))})")


def _scatter_start_point(self, val_init):
    self.ax['Z'].scatter(val_init[0], val_init[1], s=self.size+1, c=[0])


def _scatter_trajectory(self, val, color, cmap):
    self.ax['Z'].scatter(val[0,:], val[1,:], s=self.size, c=color, cmap=cmap)


def _prepare_plot(self):
    for coord, r0, r1, x_label, y_label in [
        ('Z', 0, 1, self.xlabel, self.ylabel),
    ]:

        self.ax[coord].set_title(f'{self.Titulo}')
        if self.Rango is not None:
            self.ax[coord].set_xlim(self.Rango[r0,:])
            self.ax[coord].set_ylim(self.Rango[r1,:])
        self.ax[coord].set_xlabel(f'{x_label}')
        self.ax[coord].set_ylabel(f'{y_label}')
        self.ax[coord].grid()
```
