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
        voices_en_US = [
            ("Install updates ", "install_updates"), 
            ("Enable Partner repository", "enable_partner"),
            ("Enable PPA (add-apt-repository)", "enable_ppa"),
            ("Install Elementary Tweaks", "install_elementary_tweaks"),
            ("Install multimedia codecs ", "install_multimediacodecs"), 
            ("Install Eddy (deb installer) ", "install_eddy"), 
            ("Install Telegram ", "install_telegram"), 
            ("Install System Monitor ", "install_monitor"), 
            ("Install LibreOffice ", "install_libreoffice"), 
            ("Remove Epiphany Browser ", "remove_epiphany"), 
            ("Install Firefox ", "install_firefox"), 
            ("Install Chromium ", "install_chromium"), 
            ("Install snapd (for snap packages)", "install_snapd"), 
            ("Install Redshift (eye protection) ", "install_redshift"), 
            ("Add .rar support ", "install_rar"), 
            ("Add .zip support ", "install_zip"), 
            ("Install proprietary drivers", "install_drivers"),
            ("Install more applications ", "launch_appcenter"), 
        ]
        voices_it_IT = [
            ("Installa aggiornamenti", "install_updates"), 
            ("Abilita Partner repository", "enable_partner"),
            ("Abilita PPA (add-apt-repository)", "enable_ppa"),
            ("Installa Elementary Tweaks", "install_elementary_tweaks"),
            ("Installa codec multimediali", "install_multimediacodecs"),
            ("Installa Eddy (deb installer) ", "install_eddy"), 
            ("Installa Telegram ", "install_telegram"), 
            ("Installa Monitor di sistema ", "install_monitor"), 
            ("Installa LibreOffice ", "install_libreoffice_it"),
            ("Rimuovi Browser Epiphany ", "remove_epiphany"),  
            ("Installa Firefox ", "install_firefox_it"), 
            ("Installa Chromium ", "install_chromium"), 
            ("Installa snapd (per pacchetti snap)", "install_snapd"), 
            ("Installa Redshift (protezione occhi) ", "install_redshift"), 
            ("Aggiungi supporto .rar ", "install_rar"), 
            ("Aggiungi supporto .zip ", "install_zip"), 
            ("Installa driver proprietari", "install_drivers_it"),
            ("Installa altre applicazioni ", "launch_appcenter"), 
        ]
        
        # Define functions for each menu voice
        def install_elementary_tweaks(self):
            helper.pkg_install("software-properties-common", E)
            helper.pkg_add_repo("philip.scott/elementary-tweaks", E)
            helper.pkg_update(E)
            helper.pkg_install("elementary-tweaks", E)

        def install_updates(self):
            helper.pkg_update(E)
            helper.pkg_sys_upgrade(E)

        def enable_partner(self):
            helper.do('sudo sed -i.bak "/^# deb .*partner/ s/^# //" /etc/apt/sources.list', True)
            helper.pkg_update(E)

        def install_multimediacodecs(self):
            helper.pkg_install("ubuntu-restricted-extras", E)
            helper.pkg_update(E)

        def enable_ppa(self):
            helper.pkg_install("software-properties-common", E)
            helper.pkg_update(E)
        
        def install_telegram(self):
            helper.pkg_install("software-properties-common", E)
            helper.pkg_add_repo("atareao/telegram", E)
            helper.pkg_update(E)
            helper.pkg_install("telegram", E)

        def install_eddy(self):
            helper.pkg_install("com.github.donadigo.eddy", E)
            helper.pkg_update(E)

        def install_drivers(self):
            helper.do("ubuntu-drivers autoinstall", True)
            helper.info("Reboot required!")

        def install_drivers_it(self):
            helper.do("ubuntu-drivers autoinstall", True)
            helper.info("Riavvio richiesto!")

        def install_monitor(self):
            helper.pkg_install("com.github.stsdc.monitor", E)
            helper.pkg_update(E)

        def install_libreoffice(self):
            helper.pkg_install("libreoffice", E)
            helper.pkg_update(E)

        def install_libreoffice_it(self):
            helper.pkg_install("libreoffice libreoffice-l10n-it", E)
            helper.pkg_update(E)

        def remove_epiphany(self):
            helper.pkg_remove("epiphany-browser", E)
            helper.pkg_update(E)

        def install_firefox(self):
            helper.pkg_install("firefox", E)
            helper.pkg_update(E)

        def install_firefox_it(self):
            helper.pkg_install("firefox firefox-locale-it", E)
            helper.pkg_update(E)

        def install_chromium(self):
            helper.pkg_install("chromium-browser chromium-browser-l10n", E)
            helper.pkg_update(E)

        def install_snapd(self):
            helper.pkg_install("snapd", E)
            helper.pkg_update(E)

        def install_redshift(self):
            helper.pkg_install("redshift redshift-gtk", E)
            helper.pkg_update(E)

        def install_rar(self):
            helper.pkg_install("rar urar", E)
            helper.pkg_update(E)

        def install_zip(self):
            helper.pkg_install("unzip", E)
            helper.pkg_update(E)

        def launch_appcenter(self):
            helper.pkg_install("screen", E)
            helper.do("screen -d -m appcenter")
else:
    helper.not_compatible()

# Load script
pi = PostInstall()
try:
    voices = eval('pi.voices_' + distro.lang)
except AttributeError:
    voices = pi.voices_en_US
helper.steps(voices, pi)
