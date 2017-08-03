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

import json
from hashlib import sha256

config = {}

def load(fp):
    global config
    config = json.load(fp)
    for out in config['out']:
        if out.get('inpass'):
            out['inpass'] = sha256(out['inpass'].encode()).digest()
        else:
            out['inpass'] = b''
        if out.get('outpass'):
            out['outpass'] = sha256(out['outpass'].encode()).digest()
        else:
            out['outpass'] = b''
