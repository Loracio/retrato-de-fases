try:
    __PHASE_DIAGRAMS_IMPORTED__
except NameError:
    __PHASE_DIAGRAMS_IMPORTED__= False

if not __PHASE_DIAGRAMS_IMPORTED__:
    from .phase_portrait import PhasePortrait
    from .funcion1D import Funcion1D
    from .nullclines import Nullcline2D
    
__PHASE_DIAGRAMS_IMPORTED__ = True