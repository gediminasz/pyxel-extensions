from functools import wraps
import reprlib


class reducer:
    def __init__(self, f, args, kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs

    def __call__(self, state):
        return self.f(state, *self.args, **self.kwargs)

    def __repr__(self):
        return f'<{self.f.__name__} {reprlib.repr(self.args)} {reprlib.repr(self.kwargs)}>'


def action(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return reducer(f, args, kwargs)
    return wrapper
