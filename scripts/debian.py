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
import sys
import os

g = False

for px in sys.argv:
    if px == '-gtk':
        g = True

# Define the package manager
E = "apt"

helper.title("Debian")
helper.author("Mirko Brombin")
helper.website("https://linuxhub.it")

# Check for release
distro = helper.get_distro()
helper.warning("The script for Debian has not been tested yet.")
helper.warning("Production usage is not recommended at this time.")
if distro.release in ["9.1.0"]:
    class PostInstall:
        global E
        # Define menu voices
        voices_en_US = [
            ("Install updates ", "install_updates"), 
            ("Install add-apt-repository", "enable_ppa"),
            ("Install GDebi (deb installer) ", "install_gdebi"), 
            ("Install Qapt (deb installer) ", "install_qapt"),
            ("Install GNOME (DE)", "install_gnome"), 
            ("Install GNOME (DE)", "install_gnome"), 
            ("Install KDE (DE)", "install_kde"), 
            ("Install XFCE (DE)", "install_xfce"), 
            ("Install MATE (DE)", "install_mate"), 
            ("Install LXDE (DE) ", "install_lxde"), 
            ("Install Cinnamon (DE) ", "install_cinnamon"), 
            ("Install Budgie (DE) ", "install_budgie"), 
            ("Install Enlightenment (DE) ", "install_enlightenment"), 
            ("Install Openbox (WM) ", "install_openbox"), 
            ("Install Fluxbox (WM) ", "install_fluxbox"), 
            ("Install multimedia codecs ", "install_multimediacodecs"),
            ("Install Microsoft core Fonts ", "install_mscorefonts"),
        ]
        voices_it_IT = [
            ("Installa aggiornamenti", "install_updates"), 
            ("Installa add-apt-repository", "enable_ppa"),
            ("Installa GDebi (deb installer)", "install_gdebi"), 
            ("Installa Qapt (deb installer) ", "install_qapt"), 
            ("Installa GNOME (DE)", "install_gnome"), 
            ("Installa KDE (DE)", "install_kde"), 
            ("Installa XFCE (DE)", "install_xfce"), 
            ("Installa MATE (DE)", "install_mate"), 
            ("Installa LXDE (DE) ", "install_lxde"), 
            ("Installa Cinnamon (DE) ", "install_cinnamon"), 
            ("Installa Budgie (DE) ", "install_budgie"), 
            ("Installa Enlightenment (DE) ", "install_enlightenment"), 
            ("Installa Openbox (WM) ", "install_openbox"), 
            ("Installa Fluxbox (WM) ", "install_fluxbox"), 
            ("Installa codec multimediali", "install_multimediacodecs"),
            ("Installa Microsoft core Fonts ", "install_mscorefonts"),
        ]
        
        # Define functions for each menu voice
        def install_updates(self, g=False):
            helper.pkg_update(E)
            helper.pkg_sys_upgrade(E)

        def enable_ppa(self, g=False):
            helper.pkg_install("software-properties-common", E)
            helper.pkg_update(E)

        def install_gdebi(self, g=False):
            helper.pkg_install("gdebi", E)
            helper.pkg_update(E)

        def install_qapt(self, g=False):
            helper.pkg_install("qapt-deb-installer", E)
            helper.pkg_update(E)

        def install_gnome(self, g=False):
            helper.pkg_install("gnome", E)
            helper.pkg_update(E)

        def install_kde(self, g=False):
            helper.pkg_install("kde-full", E)
            helper.pkg_update(E)

        def install_xfce(self, g=False):
            helper.pkg_install("xfce4 xfce4-goodies", E)
            helper.pkg_update(E)

        def install_mate(self, g=False):
            helper.pkg_install("mate-desktop-environment", E)
            helper.pkg_update(E)

        def install_lxde(self, g=False):
            helper.pkg_install("lxde", E)
            helper.pkg_update(E)

        def install_cinnamon(self, g=False):
            helper.pkg_install("cinnamon", E)
            helper.pkg_update(E)

        def install_lxqt(self, g=False):
            helper.pkg_install("lxqt", E)
            helper.pkg_update(E)

        def install_budgie(self, g=False):
            helper.pkg_install("budgie-desktop", E)
            helper.pkg_update(E)

        def install_openbox(self, g=False):
            helper.pkg_install("openbox menu", E)
            helper.pkg_update(E)

        def install_fluxbox(self, g=False):
            helper.pkg_install("fluxbox", E)
            helper.pkg_update(E)

        def install_multimediacodecs(self, g=False):
            self.enable_ppa()
            helper.pkg_add_repo("'deb http://www.deb-multimedia.org stretch main non-free'", E)
            helper.pkg_install("deb-multimedia-keyring libdvdcss2", E)
            helper.pkg_update(E)

        def install_mscorefonts(self, g=False):
            helper.do("mkdir temp", True)
            helper.do("cd temp", True)
            helper.do("wget http://ftp.de.debian.org/debian/pool/contrib/m/msttcorefonts/ttfmscorefonts-installer_3.6_all.deb", True)
            helper.do("dpkg --install ttf-mscorefonts-installer_3.6_all.deb", True)
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
