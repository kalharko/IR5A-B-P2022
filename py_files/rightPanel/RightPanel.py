
from kivy.uix.widget import Widget
from kivy.properties import (
    ObjectProperty
)



class RightPanel(Widget):
    gameData = ObjectProperty()

    def load_chats(self, gamepath) :
        self.chat.load_messages()
        self.diceResult.load_messages()

    def on_gameData(self, caller=None, new_value=None) :
        self.chat.gameData = self.gameData
        self.diceResult.gameData = self.gameData
