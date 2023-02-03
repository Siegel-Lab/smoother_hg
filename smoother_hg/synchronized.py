import threading
from functools import wraps

global lock
lock = threading.Lock()

def synchronized(func):
    ''' 
    This decorator limits the number of simultaneous Threads to one
    '''
    def wrapped(*args):
        with lock:
            return func(*args)
    return wrapped