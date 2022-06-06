from kivy.uix.widget import Widget
from kivy.properties import (StringProperty, ObjectProperty)

import os


class DiceResult(Widget):
    gameData = ObjectProperty(None)

    def load_messages(self):
        self.messageManager.load_messages(os.path.join(self.gameData.chat_dir, 'dice_results.txt'))
