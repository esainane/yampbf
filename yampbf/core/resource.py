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
        pass
