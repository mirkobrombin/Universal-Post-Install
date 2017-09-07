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

import os
import re
import sys
import imp
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

# Dummy function that performs a command in the system terminal
def do(command, sudo = False):
    if sudo:
        command = "sudo " + command
    return commands.getstatusoutput(command)[1]

def exit():
    do('exit')
    quit()
    return

def shorten(s, subs):
    i = s.index(subs)
    return s[:i+len(subs)-1]

# This function reproduces the steps of the loaded PostInstall script
def steps(voices, pi):
    distro = get_distro()
    info("Detected " + distro.name + " - " + distro.codename + " - " + distro.release)
    voices = [('Quit', '')] + voices
    menu = ""
    index = 0
    for voice in voices:
        menu = menu + "[" + str(index) + "] " + voice[0] + "\n"
        index += 1
    key=True
    while key:
        print "\n" + menu
        key=raw_input("Select operation:") 
        if key.isdigit():
            if key == "0":
                info("Goodbye!") 
                sys.exit()
            try:
                if voices[int(key)]:
                    bold("Loading: " + voices[int(key)][0] + "\n")
                    exec "pi." + voices[int(key)][1] + "()"
                    success("Done!")
                    bold("Select another voice")
            except IndexError:
                warning("Not a valid choice! Try again!\n")
        else:
            warning("Type a number!\n")

# This function returns a template with current distribution information
def get_distro():
    distro = models.Distro()
    distro.name = do("lsb_release -i 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-")
    distro.codename = do("lsb_release -c 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-")
    distro.release = do("lsb_release -r 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-")
    distro.lang = shorten(do("echo $LANG"), '.')
    return distro

# These are the functions that interact with the distribution packet manager
def pkg_add_repo(repo, engine):
    info("Adding repository " + repo + "..")
    if engine == "apt":
        return do("add-apt-repository ppa:" + repo + " -y", True)
    if engine == "dnf":
        do("dnf config-manager --add-repo " + repo + " -y", True)
        return do("dnf config-manager --set-enabled " + repo + " -y", True)
    if engine == "pacman":
        print "Use helper.do(command, sudo) instead of this function."
        return False

def pkg_update(engine):
    info("Updating..")
    if engine == "apt":
        return do("apt update", True)
    if engine == "dnf":
        return do("dnf update", True)
    if engine == "pacman":
        return do("pacman -Syu --noconfirm", True)

def pkg_install(pkg, engine):
    info("Installing " + pkg + "..")
    if engine == "apt":
        return do("apt install " + pkg + " -y", True)
    if engine == "dnf":
        return do("dnf install " + pkg + " -y", True)
    if engine == "pacman":
        return do("pacman -S " + pkg + " --noconfirm", True)

def pkg_remove(pkg, engine):
    info("Removing " + pkg + "..")
    if engine == "apt":
        return do("apt remove " + pkg + " -y", True)
    if engine == "dnf":
        return do("dnf remove " + pkg + " -y", True)
    if engine == "pacman":
        return do("pacman -R " + pkg + " --noconfirm", True)

def pkg_upgrade(pkg, engine):
    info("Upgrading " + pkg + "..")
    if engine == "apt":
        return do("apt upgrade -y", True)
    if engine == "dnf":
        return do("dnf upgrade -y", True)
    if engine == "pacman":
        return do("pacman -Syu --noconfirm", True)

# These are color schemes for each type of alert
def title(str):
    print shell_colors.HEADER + shell_colors.BOLD + "=== " + str + " ===" + shell_colors.END

def text(str):
    print shell_colors.NORMAL + str + shell_colors.END

def info(str):
    print shell_colors.INFO + shell_colors.BOLD + str + shell_colors.END

def bold(str):
    print shell_colors.NORMAL + shell_colors.BOLD + str + shell_colors.END

def success(str):
    print shell_colors.SUCCESS + shell_colors.BOLD + str + shell_colors.END

def error(str):
    print shell_colors.ERROR + shell_colors.BOLD + "Error: " + str + shell_colors.END

def warning(str):
    print shell_colors.WARNING + shell_colors.BOLD + str + shell_colors.END

# Dummies functions to standardize script layouts
def author(str):
    if str != "":
        text("Author: " + str)

def website(str):
    if str != "":
        text("Website: " + str + "\n")

def not_compatible():
    distro = get_distro()
    error("This script is not compatible with " + distro.name + " - " + distro.release)
    exit()

# This function loads the script for the current distribution
def load_script():
    os.system('clear')
    distro = get_distro()
    try:
        __import__("scripts." + distro.name)
    except ImportError:
        print "This distribution is currently not supported!"
