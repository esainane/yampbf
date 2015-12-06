from .resource import ResourceManager

class EventDispatcher(object):
    def __init__(self, di=None):
        self._router = di or {
        }
    async def signal(self, name, *args, **kwargs):
        if name in self._router:
            self._router[name](*args, **kwargs)
        else:
            logger.error("No signal handler found for event '%s'!" % name)
    def slot(self, name, cb):
        self._router[name] = cb

_INST = EventDispatcher()

signal = _INST.signal
slot = _INST.slot

def run():
    running = True
    def reload():
        running = False
    slot('reload', reload)
    while running:
        pass
