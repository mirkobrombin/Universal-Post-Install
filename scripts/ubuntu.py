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

helper.title("Ubuntu")
helper.author("Mirko Brombin")
helper.website("https://linuxhub.it")

# Check for release
distro = helper.get_distro()
if distro.release == "17.04":
    class PostInstall:
        global E
        # Define menu voices
        voices_en_US = [
            ("Install updates ", "install_updates"), 
            ("Enable Partner repository", "enable_partner"),
            ("Install Unity Tweak Tool", "install_unity_tweaks"),
            ("Install multimedia codecs ", "install_multimediacodecs"), 
            ("Install proprietary drivers", "install_drivers"),
            ("Install GDebi (deb installer) ", "install_gdebi"), 
            ("Install Chromium ", "install_chromium"), 
            ("Install snapd (for snap packages)", "install_snapd"), 
            ("Battery life extension with TLP ", "install_tlp"), 
            ("Install Redshift (eye protection) ", "install_redshift"), 
            ("Install more applications ", "launch_appcenter"), 
        ]
        voices_it_IT = [
            ("Installa aggiornamenti", "install_updates"), 
            ("Abilita Partner repository", "enable_partner"),
            ("Installa Unity Tweak Tool", "install_unity_tweaks"),
            ("Installa codec multimediali", "install_multimediacodecs"), 
            ("Installa driver proprietari", "install_drivers_it"),
            ("Installa GDebi (deb installer)", "install_gdebi"), 
            ("Installa Chromium ", "install_chromium"), 
            ("Installa snapd (per pacchetti snap)", "install_snapd"), 
            ("Prolunga durata batteria con TLP ", "install_tlp"), 
            ("Installa Redshift (protezione occhi) ", "install_redshift"), 
            ("Installa altre applicazioni ", "launch_appcenter"), 
        ]
        
        # Define functions for each menu voice
        def install_updates(self):
            helper.pkg_update(E)
            helper.pkg_sys_upgrade(E)

        def enable_partner(self):
            helper.do('sudo sed -i.bak "/^# deb .*partner/ s/^# //" /etc/apt/sources.list', True)
            helper.pkg_update(E)

        def install_multimediacodecs(self):
            helper.pkg_install("ubuntu-restricted-extras", E)
            helper.pkg_update(E)

        def install_drivers(self):
            helper.do("ubuntu-drivers autoinstall", True)
            helper.info("Reboot required!")

        def install_drivers_it(self):
            helper.do("ubuntu-drivers autoinstall", True)
            helper.info("Riavvio richiesto!")

        def install_gdebi(self):
            helper.pkg_install("gdebi", E)
            helper.pkg_update(E)

        def install_chromium(self):
            helper.pkg_install("chromium-browser chromium-browser-l10n", E)
            helper.pkg_update(E)

        def install_snapd(self):
            helper.pkg_install("snapd", E)
            helper.pkg_update(E)

        def install_unity_tweaks(self):
            helper.pkg_install("unity-tweak-tool", E)
            helper.pkg_update(E)

        def install_tlp(self):
            helper.pkg_install("tlp tlp-rdw", E)
            helper.do("tlp start" ,True)
            helper.pkg_update(E)

        def install_redshift(self):
            helper.pkg_install("redshift redshift-gtk", E)
            helper.pkg_update(E)

        def launch_appcenter(self):
            helper.pkg_install("screen", E)
            helper.do("screen -d -m gnome-software")
else:
    helper.not_compatible()

# Load script
pi = PostInstall()
try:
    voices = eval('pi.voices_' + distro.lang)
except AttributeError:
    voices = pi.voices_en_US
helper.steps(voices, pi)
