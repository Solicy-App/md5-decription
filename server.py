import time
import string, itertools
import hashlib
import sys
import signal
import socket
import threading


class Server:
    def __init__(self, input_hash):
        self.md5_input_hash = input_hash
        self.PORT = 5004
        self.HEADER = 64
        self.DISCONNECT = "DISCONNECT"
        self.IP = '127.0.0.1'  # local ip
        self.socket_server = socket.gethostbyname(self.IP)
        self.ADDR = (self.socket_server, self.PORT)
        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating server with data streaming
        self.SERVER.bind(self.ADDR)
        print("Socket server started on port:", self.PORT)  # just log
        self.DONE = False  # hash finding state
        self.close = 0
        self.connected_clients = []
        self.last_range = 0

    def handle_client(self, conn, addr):
        print(f"[New connection] address :: {addr} connected")
        connection = True
        while connection:
            msg_length = conn.recv(self.HEADER).decode('utf-8')  # getting data from client
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode('utf-8')
                print(f"[{addr}] {msg}")
                if self.DISCONNECT == msg:
                    connection = False
                elif msg == "get_input_hash":
                    conn.send(self.md5_input_hash.encode('utf-8'))
                elif msg == "get_new_range" and self.last_range != 32:
                    end_range = self.last_range + 4
                    if end_range > 32:
                        end_range = 32
                    last_range = f"{self.last_range}-{end_range}"
                    self.last_range = end_range
                    print(last_range)
                    conn.send(last_range.encode('utf-8'))
        conn.close()

    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        self.DONE = True
        self.close += 1
        if self.close == 2:
            sys.exit(0)

    def start(self):
        self.SERVER.listen()
        signal.signal(signal.SIGINT, self.signal_handler)
        print(f"Server listening on {self.IP}...")
        while True:
            conn, addr = self.SERVER.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            self.connected_clients.append(conn)
            print(f"[Active connections] {threading.activeCount() - 1}")


info = """
  Name            : Python Md5 Brute-force
  Created By      : Smikayel
"""
print(info)
md5_hash = input("Give md5 hash >>>")
server = Server(md5_hash)
server.start()
