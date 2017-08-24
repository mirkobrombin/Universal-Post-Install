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
from itertools import chain

class shell_colors:
    HEADER = '\033[95m'
    INFO = '\033[94m'
    SUCCESS = '\033[92m'
    NORMAL = '\033[98m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def do(command, sudo = False):
    if sudo:
        command = "sudo " + command
    return commands.getstatusoutput(command)[1]

def exit():
    return do('exit')

def steps(voices):
    voices = [('Quit', '')] + voices
    menu = ""
    index = 0
    for voice in voices:
        menu = menu + "[" + str(index) + "] " + voice[0] + "\n"
        index += 1
    key=True
    while key:
        print menu
        key=raw_input("Select operation:") 
        if key.isdigit():
            if key == "0":
                p_info("Goodbye!")  
                sys.exit()
            try:
                if voices[int(key)]:
                    p_bold("Loading: " + voices[int(key)][0] + "\n") 
                    do(voices[int(key)][1])
            except IndexError:
                p_warning("Not a valid choice! Try again!\n")
        else:
            p_warning("Type a number!\n")

def get_distro():
    distro = models.Distro()
    distro.name = do("lsb_release -i 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-")
    distro.codename = do("lsb_release -c 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-")
    distro.release = do("lsb_release -r 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-")
    return distro

def pkg_add_repo(repo, sys):
    if sys == "apt":
        return do("add-apt-repository ppa:" + repo + " -y", True)
    if sys == "dnf":
        do("dnf config-manager --add-repo " + repo + " -y", True)
        return do("dnf config-manager --set-enabled " + repo + " -y", True)
    if sys == "pacman":
        print "Use helper.do(command, sudo) instead of this function."
        return False

def pkg_update(sys):
    if sys == "apt":
        return do("apt update", True)
    if sys == "dnf":
        return do("dnf update", True)
    if sys == "pacman":
        return do("pacman -Syu --noconfirm", True)

def pkg_install(pkg, sys):
    if sys == "apt":
        return do("apt install " + pkg + " -y", True)
    if sys == "dnf":
        return do("dnf install " + pkg + " -y", True)
    if sys == "pacman":
        return do("pacman -S " + pkg + " --noconfirm", True)

def pkg_remove(pkg, sys):
    if sys == "apt":
        return do("apt remove " + pkg + " -y", True)
    if sys == "dnf":
        return do("dnf remove " + pkg + " -y", True)
    if sys == "pacman":
        return do("pacman -R " + pkg + " --noconfirm", True)

def pkg_upgrade(pkg, sys):
    if sys == "apt":
        return do("apt upgrade -y", True)
    if sys == "dnf":
        return do("dnf upgrade -y", True)
    if sys == "pacman":
        return do("pacman -Syu --noconfirm", True)

def p_title(str):
    print shell_colors.HEADER + shell_colors.BOLD + "=== " + str + " ===" + shell_colors.END

def p_text(str):
    print shell_colors.NORMAL + str + shell_colors.END

def p_info(str):
    print shell_colors.INFO + shell_colors.BOLD + "Info: " + str + shell_colors.END

def p_bold(str):
    print shell_colors.NORMAL + shell_colors.BOLD + str + shell_colors.END

def p_success(str):
    print shell_colors.SUCCESS + shell_colors.BOLD + "Success: " + str + shell_colors.END

def p_error(str):
    print shell_colors.ERROR + shell_colors.BOLD + "Error: " + str + shell_colors.END

def p_warning(str):
    print shell_colors.WARNING + shell_colors.BOLD + "Warning: " + str + shell_colors.END

def load_script():
    distro_name = get_distro().name
    try:
        __import__("scripts." + distro_name)
    except ImportError:
        print "This distribution is currently not supported!"
