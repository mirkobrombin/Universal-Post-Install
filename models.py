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

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    gui = True
except:
    gui = False

class Distro(object):
    name = ""
    codename = ""
    release = ""
    lang = ""

if gui == True:
    class Dialog(Gtk.Dialog):
    
        def __init__(self, title, text, markup, width=300, height=300, ok=True, cancel=True):
            Gtk.Dialog.__init__(self)
            self.set_title(title)
            self.set_default_size(width, height)
            if ok == True:
                self.add_button("_OK", Gtk.ResponseType.OK)
            if cancel == True:
                self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
            self.connect("response", self.on_response)
            if markup == True:
                dialog_text = Gtk.Label()
                dialog_text.set_markup(text)
            else:
                dialog_text = Gtk.Label(text)
            self.vbox.add(dialog_text)
            self.show_all()
    
        def on_response(self, dialog, response):
            if response == Gtk.ResponseType.OK:
                print("OK button clicked")
            elif response == Gtk.ResponseType.CANCEL:
                print("Cancel button clicked")
            else:
                print("Dialog closed")
    
            dialog.destroy()