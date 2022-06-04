from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, StringProperty, BooleanProperty
)



class Message(Widget) :
    content = StringProperty()
    author = StringProperty()



class MessageManager(Widget) :

    def add_message(self, author, content) :
        self.gridlayout.add_widget(Message(content=content, author=author))

    def empty_messages(self) :
        self.gridlayout.clear_widgets()


    def load_messages(self, path) :
        self.empty_messages()
        with open(path, 'r') as file :
            for line in file.readlines() :
                author = line.split(' : ')[0]
                content = line[len(author)+3:]
                self.add_message(author, content)
