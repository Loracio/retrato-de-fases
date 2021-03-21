from RetratoDeFases import *
import numpy as np

if __name__ == '__main__':

    """
    Ejemplo de uso #1: retrato de fases de un oscilador armónico (Example 5.1.1 del Strogatz)
    """
    w = 1.0 # Frecuencia angular del oscilador

    def dFOscilador(x, y):
        """
        Devuelve las expresiones del sistema bidimensional de un oscilador armónico
        """
        return y, -w*w*x

    RetratoOscilador = RetratoDeFases2D(dFOscilador, 5, 50, Densidad=1)
    RetratoOscilador.plot()

    """
    Ejemplo de uso #2: retrato de fases de un sistema en coordenadas polares (Example 7.1.1 Strogatz)
    """

    def dFPolares(r, theta):
        return 0.5*r*(1 - r*r), 1+0*theta

    RetratoPolares = RetratoDeFases2D(dFPolares, 3, 30, Polar=True, Titulo='Ciclo Límite')
    RetratoPolares.plot()

    """
    Ejemplo de uso #3: ejemplo del problema de Romeo y Julieta (Love Affairs del Strogatz).
    Podéis jugar con los parámetros e intentar los ejercicios del final del tema.
    Os dejo hecho el primero, el ejercicio 5.3.2
    """

    def dFLoveAffairs(R, J):
        return J + 0*R, -1*R + 1*J

    RetratoLoveAffairs = RetratoDeFases2D(dFLoveAffairs, 3, 30, Densidad=1.5, Titulo='Love Affairs', xlabel='R', ylabel='J')
    RetratoLoveAffairs.plot()

    """
    Ejemplo de uso #4: Rabbits vs Sheep
    """
    def dFRabbitsVsSheep(x, y):
        return x*(3-x-2*y), y*(2-x-y)

    RetratoRabbitsVsSheep = RetratoDeFases2D(dFRabbitsVsSheep, 3, 300, PrimerCuadrante=True, Densidad=2, Titulo='Rabbits vs Sheep', xlabel='Rabbits', ylabel='Sheep')
    RetratoRabbitsVsSheep.plot()

    """
    Ejemplo de uso #5: Centro no lineal
    """
    def dFCentroNoLineal(x, y):
        return y-y**3, -x-y**2

    RetratoCentroNoLineal = RetratoDeFases2D(dFCentroNoLineal, 2, 2000, Densidad=2, Titulo='Centro no lineal en (0,0)', xlabel='X', ylabel='Y')
    RetratoCentroNoLineal.plot()

    """
    Ejemplo de uso #6: Exercise 6.1.8 van der Pol oscillator
    """
    def dFVanDerPol(x, y):
        return y, -x + y*(1-x**2)

    RetratoVanDerPol = RetratoDeFases2D(dFVanDerPol, 6, 2000, Densidad=1.5, Titulo='Oscilador de van der Pol', xlabel='X', ylabel='Y')
    RetratoVanDerPol.plot()

    """
    Ejemplo de uso #7: Exercise 6.1.9 Dipole fixed point
    """
    def dFDipolo(x, y):
        return 2*x*y, y*y-x*x

    RetratoDipolo = RetratoDeFases2D(dFDipolo, 10, 2000, Densidad=1.5, Titulo='Dipolo', xlabel='X', ylabel='Y')
    RetratoDipolo.plot()

    """
    Ejemplo de uso #8: Exercise 6.1.10 Two-Eyed Monster
    """
    def dFMonster(x, y):
        return y + y*y, -0.5*x + 0.20*y - x*y + 1.20*y*y

    RetratoMonster = RetratoDeFases2D(dFMonster, 10, 2000, Densidad=1.5, Titulo='Monster', xlabel='X', ylabel='Y')
    RetratoMonster.plot()

    """
    Ejemplo de uso #9: Exercise 6.1.11 Parrot
    """
    def dFParrot(x, y):
        return y + y*y, -x + 0.20*y - x*y + 1.20*y*y

    RetratoParrot = RetratoDeFases2D(dFParrot, 10, 2000, Densidad=1.5, Titulo='Parrot', xlabel='X', ylabel='Y')
    RetratoParrot.plot()

    """
    Ejemplo de uso #10: Exercise 6.6.3 Wallpaper
    """
    def dFWallpaper(x, y):
        return np.sin(y), np.sin(x)

    RetratoWallpaper = RetratoDeFases2D(dFWallpaper, 7.5, 2000, Densidad=2, Titulo='Wallpaper', xlabel='X', ylabel='Y')
    RetratoWallpaper.plot()

    """
    Ejemplo de uso #11: Exercise 6.6.4 Computer Explorations
    """

    def dFCompEx2(x, y):
        return y - y**3, x*np.cos(y)

    RetratoCompEx2 = RetratoDeFases2D(dFCompEx2, 3, 300, Densidad=2, Titulo='Computer Explorations #2')
    RetratoCompEx2.plot()

    def dFCompEx3(x, y):
        return np.sin(y), y**2 - x

    RetratoCompEx3 = RetratoDeFases2D(dFCompEx2, 3, 300, Densidad=2, Titulo='Computer Explorations #3')
    RetratoCompEx3.plot()

    """
    Ejemplo de uso #12: Péndulo simple
    """

    def dFPendulo(theta, v):
        return v, -np.sin(theta)

    RetratoPendulo = RetratoDeFases2D(dFPendulo, 9, 900, Densidad=1.5, Titulo='Péndulo Simple', xlabel=r"$\Theta$", ylabel=r"$\dot{\Theta}$")
    RetratoPendulo.plot()

    """
    Ejemplo de uso #13: Péndulo simple amortiguado
    """

    def dFPenduloAmortiguado(theta, v):
        return v, -0.75*v-np.sin(theta)

    RetratoPenduloAmortiguado = RetratoDeFases2D(dFPenduloAmortiguado, 4, 400, Densidad=2, Titulo='Péndulo Amortiguado', xlabel=r"$\Theta$", ylabel=r"$\dot{\Theta}$")
    RetratoPenduloAmortiguado.plot()