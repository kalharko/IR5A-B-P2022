# echo-client.py

import socket, time, _thread, sys, select



class ClientConnection() :
    def __init__(self, queue_server, queue_game):
        self.queue_server = queue_server
        self.queue_game = queue_game
        self.thread = _thread.start_new_thread(self.run, ())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        # IP address
        IP_address = "127.0.0.1"
        # port number
        Port = 65432
        self.server.connect((IP_address, Port))

        self.running = True
        while self.running:
            # maintains a list of possible input streams
            sockets_list = [sys.stdin, self.server]

            """ There are two possible input situations. Either the
            user wants to give manual input to send to other people,
            or the server is sending a message to be printed on the
            screen. Select returns from sockets_list, the stream that
            is reader for input. So for example, if the server wants
            to send a message, then the if condition will hold true
            below.If the user wants to send a message, the else
            condition will evaluate as true"""
            read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

            for socks in read_sockets:
                if socks == self.server:
                    message = socks.recv(2048)
                    print (message.decode('utf-8'))
                else:
                    message = sys.stdin.readline()
                    self.server.send(bytes(message, 'utf-8'))
                    sys.stdout.write("<You>")
                    sys.stdout.write(message)
                    sys.stdout.flush()

            # Accepts tasks from queues
            while not self.queue_server.empty() :
                print('queue_server.get()')
                work = self.queue_server.get()
                print(f'server working on : {work}')

                if work == 'quit' :
                    self.server.close()
                    self.running = False
                    print('running = Fasle')

                self.queue_server.task_done()


