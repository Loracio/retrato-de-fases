from inspect import signature

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
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

class RangoInvalid(RetratoExceptions):
    def __init__(self, text):
        super().__init__(f"El rango no es válido: {text}")