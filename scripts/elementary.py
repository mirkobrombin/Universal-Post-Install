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

helper.title("ElementaryOS post installation script by https://linuxhub.it")

# Check for release
if helper.get_distro().codename == "loki":
    helper.info("Loki detected")
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
            helper.info("Installing dependence: software-properties-common")
            helper.pkg_install("software-properties-common", E)
            helper.info("Adding repository: philip.scott/elementary-tweaks")
            helper.pkg_add_repo("philip.scott/elementary-tweaks", E)
            helper.info("Updating..")
            helper.pkg_update(E)
            helper.info("Installing: elementary-tweaks")
            helper.pkg_install("elementary-tweaks", E)

        def install_gimp(self):
            helper.info("Updating..")
            helper.pkg_update(E)
            helper.info("Installing: gimp")
            helper.pkg_install("gimp", E)

        def install_thunderbird(self):
            helper.info("Updating..")
            helper.pkg_update(E)
            helper.info("Installing: thunderbird")
            helper.pkg_install("thunderbird", E)
else:
    helper.warning("This script is not compatible with " + helper.get_distro().codename)
    helper.exit()

# Load script
pi = PostInstall()
helper.steps(pi.voices, pi)
