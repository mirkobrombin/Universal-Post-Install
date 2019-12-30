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
E = "yum"

helper.title("Centos")
helper.author("Mirko Brombin")
helper.website("https://linuxhub.it")

supported_versions = [
    "7 (Core)"
]

# Check for release
distro = helper.get_distro()
helper.warning("This script is intended for use in server environments.")
if distro.release in supported_versions:
    class PostInstall:
        global E
        # Define menu voices
        voices_en_US = [
            ("Install updates", "install_updates"),
            ("Install EPEL repo", "install_epel"),
            ("Install postfix", "install_postfix"),
            ("Install dovecot", "install_dovecot"),
            ("Install nginx", "install_nginx"),
            ("Install apache2", "install_apache"),
            ("Install php-fpm", "install_php_fpm"),
        ]
        voices_it_IT = [
            ("Installa aggiornamenti", "install_updates"),
            ("Installa repo EPEL", "install_epel"),
            ("Installa postfix", "install_postfix"),
            ("Installa dovecot", "install_dovecot"),
            ("Installa nginx", "install_nginx"),
            ("Installa apache2", "install_apache"),
            ("Installa php-fpm", "install_php_fpm"),
        ]
        
        # Define functions for each menu voice
        def install_updates(self, g=False):
            helper.pkg_update(E)
            helper.pkg_sys_upgrade(E)

        def install_epel(self, g=False):
            helper.pkg_install("epel-release", E)
            helper.pkg_update(E)

        def install_postfix(self, g=False):
            helper.pkg_install("postfix", E)
            helper.pkg_update(E)

        def install_dovecot(self, g=False):
            helper.pkg_install("dovecot", E)
            helper.pkg_update(E)

        def install_nginx(self, g=False):
            helper.do("cat >/etc/yum.repos.d/nginx.repo <<EOL\
[nginx]\
name=nginx repo\
baseurl=http://nginx.org/packages/mainline/centos/7/$basearch/\
gpgcheck=0\
enabled=1\
EOL")
            helper.pkg_update(E)
            helper.pkg_install("nginx", E)

        def install_apache(self, g=False):
            helper.pkg_install("httpd", E)
            helper.pkg_update(E)

        def install_php_fpm(self, g=False):
            helper.pkg_install("php-fpm", E)
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
