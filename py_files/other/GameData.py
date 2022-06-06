import os, json
from turtle import position


class GameData:
    def __init__(self):
        self.username = None
        self.network_role = None
        self.game_dir = None
        self.data = None
        self.tokens = None
        self.maps_dir = None
        self.tokens_dir = None
        self.data_dir = None
        self.chat_dir = None

    def set_game_dir(self, path):
        self.game_dir = path
        self.maps_dir = os.path.join(self.game_dir, 'Maps')
        self.tokens_dir = os.path.join(self.game_dir, 'Tokens')
        self.data_dir = os.path.join(self.game_dir, 'data.tkt')
        self.chat_dir = os.path.join(self.game_dir, 'Chats')

    def load(self):

        if self.game_dir == None:
            return 'GameData load() error : game_dir not set'

        # Load general information
        self.data = {}
        with open(os.path.join(self.game_dir, 'game_data.txt'), 'r') as file:
            for line in file.readlines():
                self.data[line.split(' : ')[0]] = line[len(line.split(' : ')[0])+3:].rstrip('\n')

        # Load Tokens
        self.tokens = []
        with open(os.path.join(self.tokens_dir, 'tokens.txt'), 'r') as file:
            for line in file.readlines():
                if line == '|\n':
                    self.tokens.append({})
                else:
                    self.tokens[-1][line.split(' : ')[0]] = line[len(line.split(' : ')[0])+3:].rstrip('\n')
        # convert position attribute of tokens from string to list
        for token in self.tokens:
            token['position'] = token['position'].lstrip('[').rstrip(']').split(',')
            token['position'][0] = int(token['position'][0])
            token['position'][1] = int(token['position'][1])

    def save(self):
        # Save general information
        with open(os.path.join(self.game_dir, 'game_data.txt'), 'w') as file:
            for item in self.data.items():
                line = item[0] + ' : ' + item[1] + '\n'
                file.write(line)

        # Save Tokens
        with open(os.path.join(self.tokens_dir, 'tokens.txt'), 'w') as file:
            for token in self.tokens:
                file.write('|\n')
                for item in token.items():
                    line = item[0] + ' : ' + str(item[1]) + '\n'
                    file.write(line)

    def change_map(self, new_map_path):
        pass
