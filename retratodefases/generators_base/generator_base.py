from random import random

import numpy as np

from ..exceptions import *
from ..utils import utils


class _Generator_():
    def __init__(self, portrait, dF, dimension, max_values, *, dF_args=None, initial_values=None, thermalization=None, **kargs):
        self.portrait = portrait
        self.dF = dF
        self.dimension = dimension
        self.max_values = max_values
        self.thermalization = thermalization if thermalization is not None else 0

        self.dF_args = dF_args.copy()
        if utils.is_number(initial_values):
            initial_values = [initial_values]

        if initial_values is None or len(initial_values) < self.dimension:
            aux = [random() for i in range(dimension)]
            self.initial_value = np.array(aux)
        else:
            self.initial_value = np.array(tuple(map(float, initial_values)))

        self.position = self.initial_value.copy()
        

    # Métodos que deben sobreescribirse

    def _next(self):
        '''Genera a partir de `self.position` el siguiente valor de `self.position`'''
        ...

    def save(self, index):
        '''Guarda `self.position` de la manera conveniente para el tipo de representación'''
        ...

    def clear_values(self):
        '''Borra las listas que guardan la información guardada por `self.save`'''
        ...
        
    def _check_limit_cicle(self, _delta):
        '''(Opcional) Comprueba que se esté en un ciclo límite'''
        return False
     

    # Métodos generales
    def compute_all(self, *, save_freq=1, limit_cicle_check=False, delta=0.01):
        '''
        Computes `RungeKutta.max_values` and saves them. If `save_freq` is given it saves them every that amount.
        Returns the number of points calculated
        If not, it saves them every `RungeKutta.save_freq` times, 1 by default.
        '''
        for i in range(self.thermalization):
            self._next()

        return self.Nnext(self.max_values, save_freq=save_freq, limit_cicle_check=limit_cicle_check, delta=delta)

    def _create_values_array(self, *, max_values: int = None):
        if max_values is not None:
            self.max_values = max_values
        return np.zeros([self.dimension, self.max_values])

    def Nnext(self, number, *, save_freq=1, limit_cicle_check=False, delta):
        '''
        Computes next `number` pairs of position and velocity values and saves them. Returns the number of points calculated.
        If `save_freq` is given it saves the save_freq'th pair each time.
        '''
        if save_freq is not None:
            self.save_freq = save_freq
        
        if limit_cicle_check is False:
            for i in range(number):
                self.next(index=i)
            return
        
        for i in range(limit_cicle_check):
            self.next(index=i)
        if self._check_limit_cicle(delta):
            return i
        for j in range(number-limit_cicle_check):
            self.next(index=i + j)
            

    def next(self, *, index=1):
        '''
        Computes next pair of position and velocity values and saves it. If `save_freq` is given it saves the save_freq'th next.
        '''
        for j in range(self.save_freq):
            self._next()
        self.save(index)