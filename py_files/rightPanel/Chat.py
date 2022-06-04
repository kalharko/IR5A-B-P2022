
from kivy.uix.widget import Widget
from kivy.properties import (StringProperty, ObjectProperty)
import os

class Chat(Widget):
    gameData = ObjectProperty(None)
    path = StringProperty(os.path.join('Chats', 'general_chat.txt'))

    def on_text(self) :
        if len(self.chat_input.text) != 0 and self.chat_input.text[-1] == '\n' :
            with open(os.path.join(self.gameData.chat_dir, 'general_chat.txt'), 'a') as file :
                file.write(self.gameData.username +' : '+ self.chat_input.text)
                print('write', self.chat_input.text)
            self.chat_input.text = ''
            self.messageManager.load_messages(os.path.join(self.gameData.chat_dir, 'general_chat.txt'))

    def load_messages(self) :
        self.messageManager.load_messages(os.path.join(self.gameData.chat_dir, 'general_chat.txt'))
