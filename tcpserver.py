'''
FBoT, Foo or Bar over TLS.
Copyright (C) 2017  yvbbrjdr

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import socket
import ssl
import tunnel
import config
import log

class TCPServer(object):
    def __init__(self):
        self.config = config.config['in']
        self.isTLS = self.config['type'] == 'tls'
        if self.isTLS:
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.load_cert_chain(certfile = self.config['cert'], keyfile = self.config['key'])
        self.socket = socket.socket()
        self.socket.bind((self.config['addr'], self.config['port']))

    def listen(self):
        self.socket.listen()
        log.log('Server is listening at %s:%d' % (self.config['addr'], self.config['port']))
        while True:
            clientSocket, _ = self.socket.accept()
            if self.isTLS:
                try:
                    clientSocket = self.context.wrap_socket(clientSocket, server_side = True)
                except:
                    clientSocket.close()
                    continue
            tunnel.Tunnel(clientSocket).start()

    def __del__(self):
        self.socket.close()
