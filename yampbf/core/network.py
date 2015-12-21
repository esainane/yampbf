import re
import ssl
import socket
import logging
import threading
from .events import signal

class IrcSocket(object):
    '''
    Base IrcSocket class.
    Consists of a few basic functions aside from sending/receiving.
    Sending NICK, USER, message parsing, and sending PONG responses.
    '''
    ircmsg = re.compile(r"(?P<prefix>:\S+ )?(?P<command>(\w+|\d{3}))(?P<params>( [^:]\S+)*)(?P<postfix> :.*)?")

    def __init__(self, b_size = 1024):
        self.socket = None
        self.incomplete_buffer = ''
        self.buffer_size = b_size
        self._connected = False

    def connect(self, address, nick, ident, server, realname, insecure=False):
        '''
        Connect to a server.
        Sends NICK and USER messages.
        '''
        if self._connected:
            return
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not address[1] == 6667:
            self.socket = ssl.wrap_socket(self.socket)
        self.socket.connect(address)
        self.send('NICK %s' % nick)
        self.send('USER %s %s %s :%s' % (nick, ident, server, realname))
        self._connected = True
        signal('handshakedone', self)
        threading.Thread(target=self.run).start()

    def send(self, line, encoding="utf-8"):
        '''
        Send a line to the server.
        Formatted as required by rfc 1459
        '''
        print('< %s' % line)
        line = line.replace('\r', '').replace('\n', '') + '\r\n'
        totalsent = 0
        while totalsent < len(line):
            sent = self.socket.send(line[totalsent:].encode(encoding))
            if sent is 0 :
                raise RuntimeError('Socket connection broken')
            totalsent = totalsent + sent

    def recv(self):
        '''
        Receives data from the server.
        '''
        buffer_size = self.buffer_size
        d = self.socket.recv(buffer_size)
        data = d.decode('utf-8', 'replace')
        print('> %s' % data)
        return data

    def process_data(self, data):
        '''
        Read a stream of data, splitting it into messages seperated by \r\n.
        The last incomplete message (if any) will be stored in the incomplete
        buffer variable to be used in the next read of the data stream
        '''
        if self.incomplete_buffer:
            data = self.incomplete_buffer + data
            self.incomplete_buffer = ''

        if data[-2:] is '\r\n':
            split_data = data.split('\r\n')
        else:
            split_data = data.split('\r\n')
            self.incomplete_buffer = split_data.pop(-1)

        return split_data

    def parse_message(self, message):
        '''
        Utility method turning an ircmsg into a nicely formatted tuple, for ease of use.
        '''
        logging.debug(message)
        m = self.ircmsg.match(message)
        if not m:
            logging.warn('Couldn\'t match message %r' % message)
            return None

        postfix = m.group('postfix')
        if postfix:
            postfix = postfix.lstrip(' ')
            postfix = postfix.lstrip(':')

        command = m.group('command')

        if command == 'PING':
            self.send('PONG %s' % postfix)
            return None

        prefix = m.group('prefix')
        if prefix:
            prefix = prefix.lstrip(' ')
            prefix = prefix.lstrip(':')

        params = m.group('params')
        if params:
            params = params.lstrip(' ')
            params = params.split(' ')

        logging.debug('Cleaned message, prefix = %r, command = %r, params = %r, postfix = %r' % (prefix, command, params, postfix))
        return (prefix, command, params, postfix)

    def run(self):
        '''
        Repeatedy get messages from the socket and signal them, one at a time
        '''
        result = self.process_data(self.recv())
        for line in result:
            cleaned_message = self.parse_message(line)
            if cleaned_message:
                signal('message', cleaned_message)
