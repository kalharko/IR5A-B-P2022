from kivy.uix.popup import Popup
from kivy.properties import (
    StringProperty
)
from os import path
from py_files.other.FileChooserPopup import FileChooserPopup

class FirstMenuPopup(Popup):
    path = StringProperty(path.join(path.abspath('.'), 'DefaultGame'))
    def launch_as_Player(self):
        self.root.role = 'client'
        self.root.game_path = self.path
        self.dismiss()

    def launch_as_GM(self):
        self.root.role = 'server'
        self.root.game_path = self.path
        self.dismiss()

    def open_file_chooser(self):
        file_chooser = FileChooserPopup()
        file_chooser.open()
        file_chooser.bind(on_dismiss=self.popup_set_path)

        file_chooser.file_chooser.path = path.abspath('.')

    def popup_set_path(self, popup):
        self.path = popup.file_chooser.path
