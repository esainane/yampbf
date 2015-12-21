'''
Resource container.

Maintains references to resources that should ideally not be reloaded.
For instance, long-running network connections, or database connections.
'''

class ResourceManager(object):
    def __init__(self, last=None):
        '''
        ResourceManager takes its previous instance. This method effectively
        decides what needs to be kept.

        Generally, everything is kept. You may wish to alter this function if
        you desire otherwise, with whatever logic is necessary.
        '''
        self._resources = last._resources if last else {}
    def resource(self, name, Func, *args, **kwargs):
        '''
        Returns the resource identified by `name' if it exists, or invokes
        Func with *args and **kwargs if it does not.
        '''
        if name not in self._resources:
            self._resources[name] = Func(*args, **kwargs)
        return self._resources[name]
