
import core, importlib

from importlib import reload

if __name__ == '__main__':
    while True:
        core.events.run()
        reload(core)
