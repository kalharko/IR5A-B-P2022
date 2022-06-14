from kivy.uix.widget import Widget
from kivy.properties import (StringProperty, ObjectProperty)

import random
import os


class DiceResult(Widget):
    gameData = ObjectProperty(None)

    def load_messages(self):
        self.messageManager.load_messages(os.path.join(self.gameData.chat_dir, 'dice_results.txt'))


def roll_dice(faces):
    return random.randint(1, faces)


def roll_dices(dices_list):
    results = []
    for number_of_rolls, faces in dices_list:
        for _ in range(0, number_of_rolls):
            results.append((faces, roll_dice(faces)))

    print(results)
