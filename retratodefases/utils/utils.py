from ..exceptions import exceptions2D

def is_number(x):
    return isinstance(x, (float,int))

def is_range(U):
    return isinstance(U, (list,tuple))

def construct_interval_1d(var):
    try:
        if is_number(var):
            return sorted([-var, var])
        if is_range(var):
             return var
    except Exception as e:
        raise exceptions2D.RangoInvalid(f"{var} como rango 1d dio el error: "+str(e))

def construct_interval_2d(var, *, depht=0):
    try:
        if is_number(var):
            if depht == 0:
                return [sorted([0, var])]*2
            elif depht == 1:
                return sorted([-var, var])
        if is_range(var):
            if depht == 0:
                return [construct_interval_2d(i, depht=depht+1) for i in var]
            if depht == 1:
                return var
    except Exception as e:
        raise exceptions2D.RangoInvalid(f"{var} como rango 2d dio el error: "+str(e))