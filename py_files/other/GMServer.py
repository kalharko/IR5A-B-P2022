import socket, sys
import threading
from threading import Thread

class GMServer:
    def __init__(self, queue_server, queue_game):
        self.queue_server = queue_server
        self.queue_game = queue_game
        self.queue_to_clients = []
        self.queue_from_clients = []
        self.threads = []
        self.list_of_clients = []
        Thread(target=self.run, daemon=True).start()
        #self.threads.append(_thread.start_new_thread(self.run, ()))

    def run(self):
        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

        """The first argument AF_INET is the address domain of the
        socket. This is used when we have an Internet Domain with
        any two hosts The second argument is the type of socket.
        SOCK_STREAM means that data or characters are read in
        a continuous flow."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, PORT))
        except socket.error as e:
            print(str(e))
        print('Server is listening..')
        self.queue_game.put('GMServer run()')

        server.listen(100)

        self.running = True
        while self.running:
            """Accepts a connection request and stores two parameters,
            conn which is a socket object for that user, and addr
            which contains the IP address of the client that just
            connected"""
            conn, addr = server.accept()

            """Maintains a list of clients for ease of broadcasting
            a message to all available people in the chatroom"""
            self.list_of_clients.append(conn)

            # prints the address of the user that just connected
            print(addr[0] + " connected")

            # creates and individual thread for every user that connects
            Thread(target=self.clientThread, daemon=True, args=(conn, addr)).start()
            #self.threads.append(_thread.start_new_thread(self.clientThread, (conn, addr)))

            # Accepts tasks from queues
            while not self.queue_server.empty():
                sys.stdout.write('queue_server.get()\n')
                work = self.queue_server.get()
                sys.stdout.write(f'GMServer working on : {work}\n')

                if work == 'quit':
                    for q in self.queue_to_clients:
                        q.put('quit')
                        q.join()

                    conn.close()
                    server.close()
                    self.running = False

                elif type(work) == str :
                    self.broadcast(work)

                self.queue_server.task_done()

    def clientThread(self, connection, addr):
        # sends a message to the client whose user object is conn
        connection.send(bytes("You are connected !", 'utf-8'))

        running = True
        while running:
                try:
                    message = connection.recv(2048)
                    if message:

                        """prints the message and address of the
                        user who just sent the message on the server
                        terminal"""
                        message_to_send = "<" + str(addr[0]) + "> " + message.decode('utf-8')
                        sys.stdout.write(message_to_send)

                        # Calls broadcast function to send message to all
                        self.broadcast(message_to_send, connection)

                    else:
                        """message may have no content if the connection
                        is broken, in this case we remove the connection"""
                        self.list_of_clients.remove(connection) # will raise bad errors
                        sys.stdout.write('thread - lost client :', connection)
                        running = False
                        return

                except:
                    continue

        connection.send(str.encode('Server is working:'))
        while True:
            data = connection.recv(2048)
            response = 'Server message: ' + data.decode('utf-8')
            if not data:
                sys.stdout.write('connexion broke from :', addr, connection.getsockname())
                break
            connection.sendall(str.encode(response))
        connection.close()

    def serverLog(self, data):
        with open('Data/log.txt', 'a') as file :
            file.write(data+'\n')

    def broadcast(self, message, source='GM'):
        message = source+':'+message

        for client in self.list_of_clients:
            if client != source:
                try:
                    client.send(bytes(message, 'utf-8'))
                except:
                    client.close()

                    # if the link is broken, we remove the client
                    sys.stdout.write('broadcast - lost client :', client)
                    self.list_of_clients.remove(client)  # will raise bad errors
