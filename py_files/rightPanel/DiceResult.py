from kivy.uix.widget import Widget
from kivy.properties import (StringProperty, ObjectProperty)

import random
import os


class DiceResult(Widget):
    gameData = ObjectProperty(None)

    def load_messages(self):
        self.messageManager.load_messages(os.path.join(self.gameData.chat_dir, 'dice_results.txt'))

    def add_messages(self, messages):

        for message in messages:
            self.messageManager.add_message(self.gameData.username, message)

    def on_enter(self):
        dices_list = parse_command(self.dice_input.text)
        results = roll_dices(dices_list)
        messages = interpret_results(results)
        self.add_messages(messages)


def sum_as_string(list_of_ints):
    """
    Takes ints and returns the string version of the sum of these ints
    :param list_of_ints: List of the ints
    :type list_of_ints: list
    :return: string of schematized sum
    """
    sum_string = ''
    for i in list_of_ints:
        sum_string = sum_string + str(i) + '+'

    return sum_string[:-1]


def interpret_results(results):
    """
    Iterates through "results" parameter, and stores results or error if there are some.
    :param results: the information of all the dice roll information, including the result.
    :type results: list
    :return: the messages that have been printed.
    """
    messages = []
    types_of_dices = {}
    for dice_info in results:
        number = dice_info[0]
        throw_infos = dice_info[1:]
        if isinstance(number, str):
            messages.append(number + ' ' + dice_info[2])
        elif number not in types_of_dices:
            types_of_dices[number] = throw_infos
    for key in types_of_dices:
        modifier = types_of_dices[key][0]
        dice_results = types_of_dices[key][1:]
        if modifier == 0:
            messages.append(str('(' + str(len(dice_results)) + 'd' + str(key) + '):'
                            + sum_as_string(dice_results)
                        + " = " + str(sum(dice_results))))
        elif modifier < 0:
            messages.append(str('(' + str(len(dice_results)) + 'd' + str(key) + '-' + str(abs(modifier)) + '):'
                            + sum_as_string(dice_results)
                        + " = " + str(sum(dice_results) + modifier)))
        else:
            messages.append(str('(' + str(len(dice_results)) + 'd' + str(key) + '+' + str(abs(modifier)) + '):'
                            + sum_as_string(dice_results)
                        + " = " + str(sum(dice_results) + modifier)))

    return messages


def parse_command(text):
    """

    :param text:
    :return:
    """
    dices_list = []
    lst = []
    for pos, char in enumerate(text):
        if char == ',':
            lst.append(pos)
    print(lst)
    prev_idx = 0
    if len(lst) > 0:
        for idx in lst:
            substring = text[prev_idx:idx]
            dices_list.append(parse_dice_throw(substring))
            prev_idx = idx+1
        substring = text[prev_idx:]
        dices_list.append(parse_dice_throw(substring))
    else:
        dices_list.append(parse_dice_throw(text))

    return dices_list


def parse_dice_throw(text):
    """

    :param text: Te command typed by the user
    :type text: str
    :return: A list of the parsed commands
    """
    text.replace(" ", "")
    d_pos = text.find('d')
    if d_pos > 0:
        try:
            before_d = int(text[0:d_pos])
            potential_plus = text[d_pos+1:].find('+')
            potential_minus = text[d_pos+1:].find('-')
            if potential_plus < 0 and potential_minus < 0:
                after_d = int(text[d_pos+1:])
                res = [before_d, after_d]
                return res
            elif potential_minus < 0:
                after_d = int(text[d_pos+1:d_pos+1+potential_plus])
                res = [before_d, after_d, int(text[d_pos+1+potential_plus+1:])]
                return res
            else:
                after_d = int(text[d_pos+1:d_pos+1+potential_minus])
                res = [before_d, after_d, - int(text[d_pos+1+potential_minus+1:])]
                return res
        except ValueError:
            return (text,
                    ': Expression not supported')
        except IndexError:
            return (text,
                    ': Expression not supported')

    else:
        return (text,
                'you have to put the expression XdX(+X)')


def roll_dice(faces: int):
    """

    :param faces: Number of faces
    :type faces: int
    :return: an int of the result of the dice roll
    """
    return random.randint(1, faces)


def roll_dices(dices_list):
    """
    This functions take a list of information about dices roll intent,
     roll the dices for each of them and returns the result
    :param dices_list: List of dices roll information
    :type dices_list: list
    :return: The same list but each member of the list has had the result added to it.
    """
    results = []
    for list in dices_list:
        number_of_rolls = list[0]
        faces = list[1]
        modifier = list[2] if len(list) == 3 else 0
        if not isinstance(number_of_rolls, str):
            dice_info = [faces, modifier]
            for _ in range(0, number_of_rolls):
                dice_info.append(roll_dice(faces))
            results.append(dice_info)
        else:
            results.append((number_of_rolls, faces))
    return results
