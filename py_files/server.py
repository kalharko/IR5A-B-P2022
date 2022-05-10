# echo-server.py

import socket
#from time import


class GMServer():
    def __init__(self, game_path, lock) :
        self.game_path = game_path
        self.lock = lock
        #self.clients_ips = []

    def run(self):
        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

        while True :
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    message = b''
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break

                        message += data
                        conn.sendall(data)

                    # adds to log
                    #self.lock.acquire()
                    self.serverLog(data)
                    #self.lock.release()

    def serverLog(self, data):
        with open('Data/log.txt', 'a') as file :
            file.write(data+'\n')




class PlayerServer():
    def __init__(self) :
        pass
