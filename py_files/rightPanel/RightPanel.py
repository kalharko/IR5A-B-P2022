
from kivy.uix.widget import Widget




class RightPanel(Widget):

    def load_chats(self, gamepath) :
        self.chat.load_messages(gamepath)
        self.diceResult.load_messages(gamepath)
