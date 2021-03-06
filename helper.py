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

import os
import re
import sys
import imp
try:
    from subprocess import getstatusoutput
except:
    from commands import getstatusoutput
import models
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
except:
    pass

from itertools import chain

try: 
    input = raw_input
except NameError: 
    pass

g = False

for px in sys.argv:
    if px == '-gtk':
        g = True

class shell_colors:
    HEADER = '\033[95m'
    INFO = '\033[94m'
    SUCCESS = '\033[92m'
    NORMAL = '\033[98m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
def exit():
    do('exit')
    quit()
    return

def shorten(s, subs):
    i = s.index(subs)
    return s[:i+len(subs)-1]

# Dummy function that performs a command in the system terminal
def do(command, sudo = False):
    if sudo:
        command = "sudo " + command
    return getstatusoutput(command)[1]

# Get file permissions
def perm(directory, set_perm=False, sudo=False):
    if set_perm == False:
        print("stat -c %a " + directory)
        return do("stat -c %a " + directory)
    else:
        if sudo == False:
            return do("chmod " + set_perm + " " + directory)
        else:
            return do("chmod " + set_perm + " " + directory, True)

# This function returns a template with current distribution information
def get_distro():
    distro = models.Distro()
    distro.name = do("lsb_release -i 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-")
    distro.codename = do("lsb_release -c 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-")
    distro.release = do("lsb_release -r 2> /dev/null | sed 's/:\t/:/' | cut -d ':' -f 2-")
    distro.lang = shorten(do("echo $LANG"), '.')
    
    if "" in [distro.name, distro.release]:
        for item in do("cat /etc/*release").split("\n"):
            if item.startswith("ID="):
                distro.name = item[4:-1]
            if item.startswith("CODENAME="):
                distro.codename = item[10:-1]
            if item.startswith("VERSION="):
                distro.release = item[9:-1]
    return distro

# This function reproduces the steps of the loaded PostInstall script
def steps(voices, pi, gtk=False):
    distro = get_distro()
    if gtk==False:
        index = 0
        voices = [('Quit', '')] + voices
        menu = ""
        for voice in voices:
            menu = menu + "[" + str(index) + "] " + voice[0] + "\n"
            index += 1
        info("Detected " + distro.name + " - " + distro.codename + " - " + distro.release)
        key=True
        while key:
            print("\n" + menu)
            key=input("Select operation:") 
            if key.isdigit():
                if key == "0":
                    info("Goodbye!") 
                    sys.exit()
                try:
                    if voices[int(key)]:
                        bold("Loading: " + voices[int(key)][0] + "\n")
                        exec ("pi." + voices[int(key)][1] + "()")
                        success("Done!")
                        bold("Select another voice")
                except IndexError:
                    warning("Not a valid choice! Try again!\n")
            else:
                warning("Type a number!\n")
    else:
        index=0
        win = Gtk.Window(title="UPI - " + distro.name + " - " + distro.codename)
        win.set_border_width(10)
        style_provider = Gtk.CssProvider()
        css = open('style.css')
        css_data = css.read()
        css.close()
        style_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), 
            style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "UPI - " + distro.name + " - " + distro.codename
        win.set_titlebar(hb) 
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        distro_title_label = Gtk.Label(distro.name)
        distro_title_label.get_style_context().add_class("distroTitle")
        vbox.pack_start(distro_title_label, True, True, 0)
        distro_description_label = Gtk.Label(distro.codename + " - " + distro.release)
        distro_description_label.get_style_context().add_class("distroDescription")
        vbox.pack_start(distro_description_label, True, True, 0)
        btn_quit = Gtk.Button.new_with_label("Quit")
        btn_quit.connect("clicked", sys.exit)
        vbox.pack_start(btn_quit, True, True, 0)
        for voice in voices:
            index += 1
            exec("btn_"+str(index)+" = Gtk.Button.new_with_label('"+voice[0]+"')")
            exec("btn_"+str(index)+".connect('clicked', pi."+voice[1]+")")
            exec("vbox.pack_start(btn_"+str(index)+", True, True, 0)")
        win.add(vbox)
        win.connect("delete-event", Gtk.main_quit)
        win.show_all()
        Gtk.main()

# These are the functions that interact with the distribution packet manager
def pkg_add_repo(repo, engine):
    info("Adding repository " + repo + "..")
    if engine == "apt":
        return do("add-apt-repository " + repo + " -y", True)
    if engine == "dnf":
        do("dnf config-manager --add-repo " + repo + " -y", True)
        return do("dnf config-manager --set-enabled " + repo + " -y", True)
    if engine == "yum":
        do("yum-config-manager --add-repo " + repo + " -y", True)
        return do("dnf config-manager --set-enabled " + repo + " -y", True)
    if engine == "pacman":
        print("Use helper.do(command, sudo) instead of this function.")
        return False

def pkg_update(engine):
    info("Updating..")
    if engine == "apt":
        return do("apt update", True)
    if engine == "dnf":
        return do("dnf update", True)
    if engine == "yum":
        return do("yum update", True)
    if engine == "pacman":
        return do("pacman -Syu --noconfirm", True)

def pkg_install(pkg, engine):
    info("Installing " + pkg + "..")
    if engine == "apt":
        return do("apt install " + pkg + " -y", True)
    if engine == "dnf":
        return do("dnf install " + pkg + " -y", True)
    if engine == "yum":
        return do("yum install " + pkg + " -y", True)
    if engine == "pacman":
        return do("pacman -S " + pkg + " --noconfirm", True)

def pkg_remove(pkg, engine):
    info("Removing " + pkg + "..")
    if engine == "apt":
        return do("apt remove " + pkg + " -y", True)
    if engine == "dnf":
        return do("dnf remove " + pkg + " -y", True)
    if engine == "yum":
        return do("yum remove " + pkg + " -y", True)
    if engine == "pacman":
        return do("pacman -R " + pkg + " --noconfirm", True)

def pkg_upgrade(pkg, engine):
    info("Upgrading " + pkg + "..")
    if engine == "apt":
        return do("apt upgrade " + pkg + " -y", True)
    if engine == "dnf":
        return do("dnf upgrade " + pkg + " -y", True)
    if engine == "yum":
        return do("yum upgrade " + pkg + " -y", True)
    if engine == "pacman":
        return do("pacman -Syu " + pkg + " --noconfirm", True)

def pkg_sys_upgrade(engine):
    info("Upgrading your system ..")
    if engine == "apt":
        return do("apt full-upgrade -y", True)
    if engine == "dnf":
        return do("dnf upgrade -y", True)
    if engine == "yum":
        return do("yum upgrade -y", True)
    if engine == "pacman":
        return do("pacman -Syu --noconfirm", True)

# These are color schemes for each type of alert
def title(str):
    print(shell_colors.HEADER + shell_colors.BOLD + "=== " + str + " ===" + shell_colors.END)

def text(str):
    print(shell_colors.NORMAL + str + shell_colors.END)

def info(str):
    print(shell_colors.INFO + shell_colors.BOLD + str + shell_colors.END)

def bold(str):
    print(shell_colors.NORMAL + shell_colors.BOLD + str + shell_colors.END)

def success(str):
    print(shell_colors.SUCCESS + shell_colors.BOLD + str + shell_colors.END)

def error(str):
    print(shell_colors.ERROR + shell_colors.BOLD + "Error: " + str + shell_colors.END)

def warning(str):
    print(shell_colors.WARNING + shell_colors.BOLD + str + shell_colors.END)

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
def load_script(type="cli"):
    distro = get_distro()
    try:
        if type == "cli":
            __import__("scripts." + distro.name.lower())
        else:
            sys.argv.append('-gtk')
            sys.argv.append(True)
            __import__("scripts." + distro.name.lower())
    except ImportError:
        print("\
            This distribution is currently not supported!\n\
            {name} {codename} - {release}".format(
                name = distro.name,
                codename = distro.codename,
                release = distro.release
            )
        )
