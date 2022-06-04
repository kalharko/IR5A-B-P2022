import os, json


class GameData() :
    def __init__(self) :
        self.username = None
        self.network_role = None

    def set_game_dir(self, path) :
        self.game_dir = path
        self.maps_dir = os.path.join(self.game_dir, 'Maps')
        self.tokens_dir = os.path.join(self.game_dir, 'Tokens')
        self.data_dir = os.path.join(self.game_dir, 'data.tkt')
        self.chat_dir = os.path.join(self.game_dir, 'Chats')

    def open(self) :
        if len(os.listdir(self.path)) == 0 :
            os.mkdir(self.maps_dir)
            os.mkdir(self.tokens_dir)

            with open(self.data_dir, 'r') as file :
                pass




"""
Data file looks like this :

Map : <name of map present in game_dir/Maps>
nb Tokens : <number of token in the game>
Name :

"""


