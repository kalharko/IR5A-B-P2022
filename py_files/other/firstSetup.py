import os


def firstSetup():
    if not 'Data' in os.listdir():
        os.mkdir('Data')

        # User preferences
        with open('Data/usr_pref.txt', 'w') as file:
            file.write('|\n|\n|\n|')
