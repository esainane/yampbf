
import core, importlib

from importlib import reload

if __name__ == '__main__':
    r = core.resource.ResourceManager()
    while True:
        core.config.init(r)
        core.events.run()
        reload(core)
        r = core.resource.ResourceManager(r)
