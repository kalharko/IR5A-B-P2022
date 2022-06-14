from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (
    NumericProperty, ColorProperty, ReferenceListProperty
)
from kivy.clock import Clock


class ContextualMenu(BoxLayout):
    x = NumericProperty(0)
    y = NumericProperty(0)
    pos = ReferenceListProperty(x, y)

    def start_vote(self):
        """

        :return:
        """
        self.disabled = True
        print("function start_vote ok")
        self.dismiss()

    def change_map(self):
        """
        """
        self.disabled = True
        print("function change_map ok")
        self.dismiss()

    def on_disabled(self, origin, new_value):
        if self.disabled:
            self.opacity = 0
        else:
            self.opacity = 1

    def test_collision(self, position):
        # Weird hack to click the childrens
        for w in self.children :
            if w.collide_point(*position) :
                try :
                    if w.text == 'create vote' :
                        self.start_vote()
                    elif w.text == 'change map' :
                        self.change_map()
                except :
                    pass #catch when it detect colision with a box layout ? but there is no box layout in self.children...
