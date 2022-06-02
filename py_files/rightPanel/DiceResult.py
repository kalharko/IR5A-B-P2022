from kivy.uix.widget import Widget
from kivy.properties import (StringProperty)

import os


class DiceResult(Widget) :
    path = StringProperty(os.path.join('Chats', 'dice_results.txt'))


    def load_messages(self, gamepath) :
        self.messageManager.file_path = os.path.join(gamepath, self.path)
        self.messageManager.load_messages()
