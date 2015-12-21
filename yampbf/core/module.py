
from .events import signal, slot

# FIXME

def message(m):
    print(m)

slot('message', message)
