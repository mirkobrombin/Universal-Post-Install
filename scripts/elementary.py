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

# Define the package manager
E = "apt"

helper.title("ElementaryOS")
helper.author("Mirko Brombin")
helper.website("https://linuxhub.it")

# Check for release
distro = helper.get_distro()
if distro.release == "0.4.1":
    class PostInstall:
        global E
        # Define menu voices
        voices = [
            ("Install Elementary Tweaks", "install_elementary_tweaks"),
            ("Install Gimp", "install_gimp"), 
            ("Install Thunderbird", "install_thunderbird"),
        ]
        
        # Define functions for each menu voice
        def install_elementary_tweaks(self):
            helper.pkg_install("software-properties-common", E)
            helper.pkg_add_repo("philip.scott/elementary-tweaks", E)
            helper.pkg_update(E)
            helper.pkg_install("elementary-tweaks", E)

        def install_gimp(self):
            helper.pkg_update(E)
            helper.pkg_install("gimp", E)

        def install_thunderbird(self):
            helper.pkg_update(E)
            helper.pkg_install("thunderbird", E)
else:
    helper.not_compatible()

# Load script
pi = PostInstall()
helper.steps(pi.voices, pi)
