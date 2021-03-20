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
    Ejemplo de uso #2: retrato de fases de un sistema en coordenadas polares (Example 6.3.2 Strogatz)
    """

    def dFPolares(r, theta):
        return 0.5*r*(1 - r*r), 1+0*theta # Si se juega con este último valor salen cosas interesantes...

    RetratoPolares = RetratoDeFases2D(dFPolares, 3, 30, Polar= True, Titulo= 'Retrato en coord. polares (Example 6.3.2)')
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
    Ejemplo de uso #4: péndulo simple
    """

    def dFPendulo(theta, v):
        return v, -np.sin(theta)

    RetratoPendulo = RetratoDeFases2D(dFPendulo, 9, 900, Densidad=1.5, Titulo='Péndulo Simple', xlabel=r"$\Theta$", ylabel=r"$\dot{\Theta}$")
    RetratoPendulo.plot()

    """
    Ejemplo de uso #5: péndulo simple amortiguado
    """

    def dFPenduloAmortiguado(theta, v):
        return v, -0.75*v-np.sin(theta)

    RetratoPenduloAmortiguado = RetratoDeFases2D(dFPenduloAmortiguado, 4, 400, Densidad=2, Titulo='Péndulo Amortiguado', xlabel=r"$\Theta$", ylabel=r"$\dot{\Theta}$")
    RetratoPenduloAmortiguado.plot()