try:
    __PHASE_DIAGRAMS_IMPORTED__
except NameError:
    __PHASE_DIAGRAMS_IMPORTED__= False

if not __PHASE_DIAGRAMS_IMPORTED__:
    from .phase_portrait import PhasePortrait
    
__PHASE_DIAGRAMS_IMPORTED__ = True