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
E = "dnf"

helper.title("Fedora")
helper.author("gstux")
helper.website("https://linuxhub.it")

supported_versions = [
    "28",
    "29",
    "30"
]
# Check for release
distro = helper.get_distro()
helper.warning("The script for Fedora has not been tested yet.")
helper.warning("Production usage is not recommended at this time.")
if distro.release in supported_versions:
    class PostInstall:
        global E
        # Define menu voices
        voices_en_US = [
            ("Install updates ", "install_updates"),
            ("Enable RPM Fusion", "enable_rpmfusion"),
            ("Install GNOME (DE)", "install_gnome"),
            ("Install KDE (DE)", "install_kde"),
            ("Install XFCE (DE)", "install_xfce"),
            ("Install MATE (DE)", "install_mate"),
            ("Install LXDE (DE)", "install_lxde"),
            ("Install Cinnamon (DE)", "install_cinnamon"),
            ("Install Openbox (WM)", "install_openbox"),
            ("Install Fluxbox (WM)", "install_fluxbox"),
            ("Install GNOME Tweak Tool", "install_tweak_tool"),
            ("Install media codecs", "install_multimediacodecs"),
        ]
        voices_it_IT = [
            ("Installa aggiornamenti ", "install_updates"),
            ("Abilita RPM Fusion", "enable_rpmfusion"),
            ("Installa GNOME (DE)", "install_gnome"),
            ("Installa KDE (DE)", "install_kde"),
            ("Installa XFCE (DE)", "install_xfce"),
            ("Installa MATE (DE)", "install_mate"),
            ("Installa LXDE (DE)", "install_lxde"),
            ("Installa Cinnamon (DE)", "install_cinnamon"),
            ("Installa Openbox (WM)", "install_openbox"),
            ("Installa Fluxbox (WM)", "install_fluxbox"),
            ("Installa GNOME Tweak Tool", "install_tweak_tool"),
            ("Installa codec multimediali", "install_multimediacodecs")
        ]

        # Define functions for each menu voice
        def install_updates(self, g=False):
            helper.pkg_update(E)
            helper.pkg_sys_upgrade(E)

        def enable_rpmfusion(self, g=False):
            helper.pkg_install("https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm", E)
            helper.pkg_update(E)

        def install_gnome(self, g=False):
            helper.pkg_install("@gnome-desktop", E)
            helper.pkg_update(E)

        def install_kde(self, g=False):
            helper.pkg_install("@kde-desktop", E)
            helper.pkg_update(E)

        def install_xfce(self, g=False):
            helper.pkg_install("@xfce", E)
            helper.pkg_update(E)

        def install_mate(self, g=False):
            helper.pkg_install("@mate-desktop-environment", E)
            helper.pkg_update(E)

        def install_lxde(self, g=False):
            helper.pkg_install("@lxde", E)
            helper.pkg_update(E)

        def install_cinnamon(self, g=False):
            helper.pkg_install("@cinnamon", E)
            helper.pkg_update(E)

        def install_lxqt(self, g=False):
            helper.pkg_install("@lxqt", E)
            helper.pkg_update(E)

        def install_openbox(self, g=False):
            helper.pkg_install("openbox obconf", E)
            helper.pkg_update(E)

        def install_fluxbox(self, g=False):
            helper.pkg_install("fluxbox", E)
            helper.pkg_update(E)

        def install_multimediacodecs(self, g=False):
            helper.pkg_install("gstreamer1-plugins-base gstreamer1-plugins-good gstreamer1-plugins-ugly gstreamer1-plugins-bad-free gstreamer1-plugins-bad-freeworld gstreamer1-plugins-bad-free-extras ffmpeg", E)
            helper.pkg_update(E)
else:
    helper.not_compatible()

# Load script
pi = PostInstall()
try:
    voices = eval('pi.voices_' + distro.lang)
except AttributeError:
    voices = pi.voices_en_US
helper.steps(voices, pi, g)
