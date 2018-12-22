import socket
from threading import *

def main():
    host = "127.0.0.1"
    port = 2233
    s = socket.socket()
    s.connect((host, port))
    while True:
        data = s.recv(2048).decode()
        data = str(data)
        print(data)
        if "-" in data:
            par = str(data).split("-")
            if par[1] in ["SUCCESS", "NOTFOUND", "Syntax"]:
                break
        inp = input().encode()
        s.send(inp)
    s.close()

if __name__ == '__main__':
    main()