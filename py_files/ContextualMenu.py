from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ColorProperty, ReferenceListProperty
)


class ContextualMenu(Widget):

    def __init__(self, ):
        Widget.__init__(self)

        x = NumericProperty(0)
        y = NumericProperty(0)
        self.pos = ReferenceListProperty(x, y)

    def start_vote(self):
        """

        :return:
        """
        print("function start_vote ok")
        pass

    def change_map(self):
        """
        """
        print("function change_map ok")
        pass


class ContextualMenuManager(Widget):
    bg_color = ColorProperty()
    sizeWanted = NumericProperty()
    is_displayed = False

    def on_touch_down(self, touch):
        """Game related contextual menu instanciation, called when player right clicks on the map"""
        menu = ContextualMenu()
        is_displayed = True
        self.add_widget(menu)
        menu.pos = touch.pos
