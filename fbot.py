#!/usr/bin/env python3

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

import argparse
import version
import config
import tcpserver

def main():
    parser = argparse.ArgumentParser(prog = 'FBoT', description = 'Foo or Bar over TLS.')
    parser.add_argument('-v', '--version', action = 'version', version='%(prog)s ' + version.version)
    parser.add_argument('config', help = 'the JSON config file to load', type = argparse.FileType('r'))
    with parser.parse_args().config as fp:
        config.load(fp)
    tcpserver.TCPServer().listen()

if __name__ == '__main__':
    main()
