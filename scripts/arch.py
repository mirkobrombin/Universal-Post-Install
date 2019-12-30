'''
   Copyright 2017 Mirko Brombin (send@mirko.pm)

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
import sys
import os

g = False

for px in sys.argv:
    if px == '-gtk':
        g = True

# Define the package manager
E = "pacman"

helper.title("Arch Linux")
helper.author("Mirko Brombin")
helper.website("https://linuxhub.it")

# Check for release
distro = helper.get_distro()
helper.warning("This script may not be stable.")
class PostInstall:
    global E
    # Define menu voices
    voices_en_US = [
        ("Install updates", "install_updates"),
    ]
    voices_it_IT = [
        ("Installa aggiornamenti", "install_updates"),
    ]
    
    # Define functions for each menu voice
    def install_updates(self, g=False):
        helper.pkg_update(E)
        helper.pkg_sys_upgrade(E)

# Load script
pi = PostInstall()
try:
    voices = eval('pi.voices_' + distro.lang)
except AttributeError:
    voices = pi.voices_en_US
helper.steps(voices, pi, g)
