"""A decorator for executing a function repeatedly.

WARNING: This is not suitable for asynchorous programming because this uses time.sleep


Example:

# Python 3+

from loop import Loop

loop = Loop(allowed_errors=[])

@loop.loop(seconds=5, minutes=5, hours=5)
def my_func():
  pass

"""



import typing
import time

from functools import wraps


class TimeTooLow(Exception):
    pass


class TimeTooHigh(Exception):
    pass


class TimeError(TimeTooLow, TimeTooHigh):
    pass


class Task:
    _iterations = _errors = 0

    def __init__(self, func, allowed_errors: list):
        if not callable(func):
            raise TypeError('Expected positional argument `func` to be a function, got %s instead'.format(type(func)))

        self._allowed_errors = allowed_errors
        self.func = func

    def status(self):
        return {'iterations': self._iterations, 'errors': self._errors}

    def execute(self, *args, **kwargs):
        try:
            self.func(*args, **kwargs)
        except Exception as e:
            if not type(e) in self._allowed_errors:
                print(f'Uncaught exception {type(e)} occurred: {e}')
            else:
                logging.warn(f'Ignoring exception {type(e)}: {e}')
                self._errors += 1


class Loop:
    def __init__(self, *args, allowed_errors: list = None, start: typing.Union[bool, callable] = True, **kwargs):
        if start and (callable(start)):
            self._can_run = start(*args, **kwargs)
        elif start:
            self._can_run = True
        else:
            self._can_run = False

        self._task = Task
        self._allowed_errors = allowed_errors

    def loop(self, *, seconds: int = 0, minutes: int = 0, hours: int = 0):
        _seconds = ((hours * 3600) + ((minutes * 60) if minutes else (seconds if seconds else 0))) if hours else \
            ((minutes * 60) if minutes else (seconds if seconds else 0))

        if _seconds < 6:
            raise TimeTooLow('Scheduled time must be above 5 seconds')

        if _seconds > 86400:
            raise TimeTooHigh('Scheduled time must be below 1 day')

        def inner(func):
            task = self._task(func, self._allowed_errors)

            @wraps
            def wrapper(*args, **kwargs):
                while self._can_run:
                    task.execute(*args, **kwargs)
                    time.sleep(_seconds)

            return wrapper
        return inner

    def run(self):
        self._can_run = True
