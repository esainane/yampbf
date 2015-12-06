from .network import IrcSocket
class IrcConnection(object):
    """
    Represents a wrapper for the network class, provides convienience methods
    for irc such as msg and join/leave channels
    """
    def __init__(self, name, server, port):
        assert server and port
        self.connection = IrcSocket()
        self.connection.connect((server, port), name, "%s@%s" % (name, server), server, name)

        self.name = name
        self.server = server
        self.port = port

    def msgs_all(self, msgs, targets):
        """
        Accepts a list of msgs to send to a list of channels
        """
        for target in targets:
            for message in msgs:
                self.msg(message, channel)

    def msg_all(self, message, targets):
        """
        Accepts a message to send to a list of channels
        """
        for target in targets:
            self.msg(message, channel)

    def msg(self, message, target):
        '''
        Send a message to a target user or channel.
        '''
        self.connection.send('PRIVMSG %s :%s' % (channel, message))

    def join(self, channel):
        '''
        Join a channel.
        The channel should contain one or more # symbols as needed.
        '''
        self.connection.send('JOIN %s' % channel)

    def quit(self, message):
        '''
        Disconnects from a server, with a given QUIT message.
        '''
        self.connection.send('QUIT :%s' % message)

    def leave(self, channel, message="Leaving."):
        '''
        Leaves a channel.
        '''
        self.connection.send('PART %s :%s' % (channel, message))
