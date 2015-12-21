
from .irc import IrcConnection
from .events import slot

def onconnect(c):
    print('connected')
    c.join("#testbawt")
    c.msg("#testbawt", "Hello, world!")

def init(r):
    print('init')
    slot('connected', onconnect)
    nick, server, port = 'bawt', 'irc.freenode.net', 6697
    namespace = '%s!%s:' % (nick, server)
    r.resource('%s connection' % namespace, IrcConnection, nick, server, port)
