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

helper.p_title("ElementaryOS post installation script by https://linuxhub.it")

if helper.get_distro().codename == "loki":
    helper.p_info("Loki detected")
else:
    helper.p_warning("This script is not compatible with " + helper.get_distro().codename)
    helper.exit()

voices = [
    ('apt update', 'sudo apt update'), 
]

helper.steps(voices)
