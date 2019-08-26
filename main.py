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
import models
import argparse
import sys
import os
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    gui = True
except:
    gui = False

if os.getuid() == 0:
    root = True
else:
    root = False

# define script args
parser = argparse.ArgumentParser(
    description='Universal Post Install by https://linuxhub.it'
)
parser.add_argument('-gtk', action='store_true', 
    help='run in GTK mode')
args = parser.parse_args()  

# start the script
if args.gtk == True:
    if gui == True:
        if root == True:
            helper.load_script(type="gtk")
        else:
            dialog = models.Dialog("UPI - Error!", 
                "The flag (-gtk) needs the program to run as sudo! <a href=\"https://github.com/mirkobrombin/Universal-Post-Install/blob/master/README.md\" " "title=\"see here\">see here</a> how to do it", 
                True,
                580, 
                200,
                True,
                False)
            dialog.run()
    else:
        helper.error("It is not possible to start in GUI mode on this system. The python-gi package is not installed.")
else:
    helper.load_script()
