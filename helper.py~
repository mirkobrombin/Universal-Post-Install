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

import platform
import sys
import subprocess
import models
import commands

so = "sudo"

def do(command):
    return commands.getstatusoutput(command)

def get_distro_info():
    distro = models.Distro()
    distro.name = do("lsb_release -i 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-")
    distro.codename = do("lsb_release -c 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-")
    distro.release = do("lsb_release -r 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-")
    return distro

print get_distro_info().release

def update(): 
	return subprocess.call([so, aptget, "update"])

# DISTRO_NAME lsb_release -i 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-
# DISTRO_CODENAME lsb_release -c 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-
# DISTRO_RELEASE lsb_release -r 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-

