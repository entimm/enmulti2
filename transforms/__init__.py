MY_TRANSFORMATIONS = []


def transformation(name, key):
    def wrapper(func):
        MY_TRANSFORMATIONS.append((name, key, func))
        return func

    return wrapper


from .simple import *
from .complex import *
