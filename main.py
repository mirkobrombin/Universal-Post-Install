#!/usr/bin/env python
'''
   Copyright 2017 Mirko Brombin (brombinmirko@gmail.com)

   This file is part of Universal Post Install.

    Universal Post Install is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Universal Post Install is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Universal Post Install.  If not, see <http://www.gnu.org/licenses/>.
'''

import helper
import argparse
import sys

# define script args
parser = argparse.ArgumentParser(
    description='Universal Post Install by https://linuxhub.it'
)
parser.add_argument('-gtk', action='store_true', 
    help='run in GTK mode (currently not supported)')
args = parser.parse_args()  

# start the script
helper.load_script()
