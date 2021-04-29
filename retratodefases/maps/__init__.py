try:
    __MAPS_IMPORTED__
except NameError:
    __MAPS_IMPORTED__= False

if not __MAPS_IMPORTED__:
    from .map import Map
    from .cobweb import Cobweb
    
__MAPS_IMPORTED__ = True