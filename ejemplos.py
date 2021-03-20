from RetratoDeFases import RetratoDeFases2D

if __name__ == '__main__':

    """
    Ejemplo de uso #1: retrato de fases de un oscilador armónico
    """
    w = 1.0 #Frecuencia angular del oscilador

    def dFOscilador(x, y):
        """
        Devuelve las expresiones del sistema bidimensional de un oscilador armónico
        """
        return y, -w*w*x

    RetratoOscilador = RetratoDeFases2D(dFOscilador, 5, 50)
    RetratoOscilador.plot()

    """
    Ejemplo de uso #2: retrato de fases de un sistema en coordenadas polares
    """

    def dFPolares(r, theta):
        return 0.5*r*(1 - r*r), 1+0*theta # Si se juega con este último valor salen cosas interesantes...

    RetratoPolares = RetratoDeFases2D(dFPolares, 3, 30, Polar= True, Titulo= 'Retrato en coord. polares')
    RetratoPolares.plot()