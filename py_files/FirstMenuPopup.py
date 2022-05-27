from kivy.uix.popup import Popup
from kivy.properties import (
    StringProperty
)
from os import path
from py_files.FileChooserPopup import FileChooserPopup

class FirstMenuPopup(Popup):
    path = StringProperty(path.abspath('.'))
    def launch_as_Player(self):
        self.root.role = 'client'
        self.dismiss()

    def launch_as_GM(self):
        self.root.role = 'server'
        self.dismiss()

    def open_file_chooser(self):
        file_chooser = FileChooserPopup()
        file_chooser.open()
        file_chooser.bind(on_dismiss=self.popup_set_path)

        file_chooser.file_chooser.path = path.abspath('.')

    def popup_set_path(self, popup):
        self.path = popup.file_chooser.path
