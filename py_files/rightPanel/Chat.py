
from kivy.uix.widget import Widget
from kivy.properties import (StringProperty, ObjectProperty, BooleanProperty)
import os


class Chat(Widget):
    gameData = ObjectProperty(None)
    path = StringProperty(os.path.join('Chats', 'general_chat.txt'))
    double_call_workaround = BooleanProperty(False)

    def on_text(self) :
        if len(self.chat_input.text) != 0 and self.chat_input.text[-1] == '\n' :
            if self.double_call_workaround :
                self.double_call_workaround = False
            else :
                with open(os.path.join(self.gameData.chat_dir, 'general_chat.txt'), 'a') as file :
                    file.write(self.gameData.username +' : '+ self.chat_input.text[:-1]+'\n')
                    self.double_call_workaround = True
            self.chat_input.text = ''
            self.messageManager.load_messages(os.path.join(self.gameData.chat_dir, 'general_chat.txt'))

    def load_messages(self) :
        self.messageManager.load_messages(os.path.join(self.gameData.chat_dir, 'general_chat.txt'))
