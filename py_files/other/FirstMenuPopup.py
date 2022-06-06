from kivy.uix.popup import Popup
from kivy.properties import (
    StringProperty
)
from os import path
from py_files.other.FileChooserPopup import FileChooserPopup


class FirstMenuPopup(Popup):
    path = StringProperty(path.join(path.abspath('.'), 'DefaultGame'))

    def launch_as_Player(self):
        self.root.gameData.role = 'client'
        self.root.gameData.set_game_dir(self.path)
        self.root.gameData.username = 'kalharko'
        self.dismiss()

    def launch_as_GM(self):
        self.root.gameData.role = 'server'
        self.root.gameData.set_game_dir(self.path)
        self.root.gameData.username = 'kalharko'
        self.dismiss()

    def open_file_chooser(self):
        file_chooser = FileChooserPopup()
        file_chooser.open()
        file_chooser.bind(on_dismiss=self.popup_set_path)

        file_chooser.file_chooser.path = path.abspath('.')

    def popup_set_path(self, popup):
        self.path = popup.file_chooser.path
