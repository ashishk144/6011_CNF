from threading import *
import os
import socket
import random
import signal
import time


def main():
    host = "127.0.0.1"
    port = 5128

    s = socket.socket()
    s.bind((host, port))

    s.listen(5)
    print("Server has started")
    while True:
        c, addr = s.accept()
        print("Connection established with :" + str(addr))
        c.send("Guess the number between 1 and 50 that I'm thinking of".encode())
        ran = int(random.randint(1,50))
        print(ran)
        thread = Thread(target = client, args = (c, ran)).start()

def client(conn, ran):
    great = "The guessed value is greater".encode()
    less = "The guessed value is lesser".encode()
    correct = "The guessed value is correct".encode()
    cnt = 0
    while True:
        cnt = cnt + 1
        data = conn.recv(2048)
        if not data:
            conn.close()
            kill()
            break
        val = int(data.decode())
        if(val > ran):
            conn.send(great)
        elif(val < ran):
            conn.send(less)
        else:
            conn.send(correct)
            conn.close()
            kill()
            return 1
        if cnt == 3:
            conn.send("Guess limit reached to max".encode())
            kill()
            conn.close()
            return 1
        
def kill():
    pid = os.getpid()
    # print(active_count())
    if active_count() == 2:
        print("going to sleep")
        time.sleep(60)
        if(active_count() == 2):
            os.kill(pid, signal.CTRL_BREAK_EVENT)

if __name__ == '__main__':
    main()