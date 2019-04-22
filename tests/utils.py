import time
from functools import partial, wraps


def _delay(func, seconds):

    @wraps(func)
    def decorate(*args, **kwargs):
        time.sleep(seconds)
        return func(*args, **kwargs)

    return decorate


delay = partial(_delay, seconds=3)
