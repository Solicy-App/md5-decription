import socket
import threading
import time
import itertools
import sys
import hashlib
import string
import json

PORT = 5004
IP = '127.0.0.1'  # local ip (computer ip)
HEADER = 64
DISCONNECT = "DISCONNECT"
ADDR = (IP, PORT)
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect(ADDR)
print("Connected to server!")
input_hash = ''
# will check
# with this symboles
# (0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
CHRS = string.printable.replace(' \t\n\r\x0b\x0c', '')
IS_DONE = False
thread_count = 4


def send(msg):
    message = msg.encode('utf-8')
    msg_length = len(message)
    send_length = str(msg_length).encode('utf-8')
    send_length += b' ' * (HEADER - len(send_length))
    CLIENT.send(send_length)
    CLIENT.send(message)


def get_input_hash():
    send("get_input_hash")
    global input_hash
    input_hash = CLIENT.recv(1024).decode('utf-8') # be sure that hash is less then 1024 bytes or change 1024 value


def disconnect():
    send(DISCONNECT)


def get_new_range():
    pass
    send("get_new_range")
    range = CLIENT.recv(1024).decode('utf-8')  # be sure that hash is less then 1024 bytes or change 1024 value
    range = range.split('-')
    return range


def is_creacked(file_check):
    with open(file_check, "r") as file:
        data = json.load(file)
    return data["finded"]


def finde_state():
    with open("chack.json", "w") as file:
        data = {"finded":  True}
        json.dump(data, file)


def attack_thread(chrs, n):
    print("\n[!] I'm at ", n, "-character")
    for xs in itertools.product(chrs, repeat=n):
        saved = ''.join(xs)
        stringg = saved
        m = hashlib.md5()
        m.update(saved.encode('utf-8'))
        print(m.hexdigest())
        if m.hexdigest() == input_hash:
            time.sleep(10)
            global IS_DONE
            IS_DONE = True
            send(f"FOUND:{stringg}")
            finde_state()
            sys.exit("Thank You !")
    print("here")
    return


def attack(range_):
    i = range_[0]
    while i < range_[1]:
        print(i, "<<<<")
        t = threading.Thread(target=attack_thread, args=("0123456789", i))
        t.start()
        i += 1
    while t.is_alive():
        continue


def start():
    global connected
    connected = True
    get_input_hash()  # getting input hash for testings
    # attack()
    while True:
        range_ = get_new_range()
        range_ = [int(range_[0]), int(range_[1])]
        attack(range_)
        if is_creacked("chack.json"):
            disconnect()

start()
disconnect()
