from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty, BooleanProperty
)



class Message(Widget) :
    content = StringProperty()
    author = StringProperty()



class MessageManager(Widget) :
    file_path = StringProperty()

    def add_message(self, author, content) :
        self.gridlayout.add_widget(Message(content=content, author=author))


    def load_messages(self) :
        """ chat file content :
        msg_author : msg_content
        """
        with open(self.file_path, 'r') as file :
            for line in file.readlines() :
                author = line.split(' : ')[0]
                content = line[len(author)+3:]
                self.add_message(author, content)
