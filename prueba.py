import RetratoDeFases as ph


w = 1.0 #Frecuencia angular del oscilador

def dF(x, y):
    return y, -w*w*x

RetratoOscilador = ph.RetratoDeFases2D(dF, 5, 50)
RetratoOscilador.plot()
