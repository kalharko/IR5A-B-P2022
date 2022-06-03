
from kivy.uix.widget import Widget
from kivy.properties import (StringProperty)
import os

class Chat(Widget):
    path = StringProperty(os.path.join('Chats', 'general_chat.txt'))

    def on_enter(self, value) :
        print("enter", value)

    def load_messages(self, gamepath) :
        self.messageManager.file_path = os.path.join(gamepath, self.path)
        self.messageManager.load_messages()
