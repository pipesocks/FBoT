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
import threading
import config
import ssl
from log import log

class Tunnel(object):

    hashLength = 32

    def __init__(self, clientSocket):
        log('connection established', clientSocket)
        self.config = config.config['out']
        self.clientSocket = clientSocket

    def start(self):
        self.clientOpen = True
        self.serverOpen = False
        self.firstPacketSent = False
        threading.Thread(target = self.clientSocketThread).start()

    def clientSocketThread(self):
        while True:
            data = self.clientSocket.recv(4096)
            if data:
                self.clientRecv(data)
            else:
                self.clientOpen = False
                self.clientSocket.close()
                if self.serverOpen:
                    self.serverSocket.shutdown(socket.SHUT_RDWR)
                break

    def serverSocketThread(self):
        while True:
            data = self.serverSocket.recv(4096)
            if data:
                self.clientSocket.send(data)
            else:
                self.serverOpen = False
                self.serverSocket.close()
                if self.clientOpen:
                    self.clientSocket.shutdown(socket.SHUT_RDWR)
                break

    def clientRecv(self, data):
        if self.firstPacketSent:
            self.serverSocket.send(data)
        else:
            self.firstPacketSent = True
            if len(data) >= Tunnel.hashLength:
                segment = data[:Tunnel.hashLength]
                bar = None
                for out in self.config:
                    if out['inpass'] == segment:
                        bar = out
                        break
                if bar:
                    self.connectToServer(bar, data[Tunnel.hashLength:])
                    return
            foo = None
            for out in self.config:
                if out['inpass'] == b'':
                    foo = out
                    break
            if foo:
                self.connectToServer(foo, data)
            else:
                log('no out found', self.clientSocket)
                self.clientSocket.shutdown(socket.SHUT_RDWR)

    def connectToServer(self, out, data):
        self.serverSocket = socket.socket()
        if out['type'] == 'tls':
            context = ssl.create_default_context()
            if out.get('ca'):
                context.load_verify_locations(out['ca'])
            self.serverSocket = context.wrap_socket(self.serverSocket, server_hostname = out['addr'])
        try:
            self.serverSocket.connect((out['addr'], out['port']))
        except:
            log('%s:%d connect failed' % (out['addr'], out['port']))
            self.clientSocket.shutdown(socket.SHUT_RDWR)
            return
        log('connect to %s:%d' % (out['addr'], out['port']), self.clientSocket)
        self.serverOpen = True
        self.serverSocket.send(out['outpass'] + data)
        threading.Thread(target = self.serverSocketThread).start()
