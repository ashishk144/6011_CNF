import csv
import socket
from threading import *

with open('data.csv', mode = 'r') as file:
    csv_reader = csv.reader(file, delimiter = ",")
    diction = {}
    for row in csv_reader:
        diction[row[0]] = [row[1], row[2]]
    keyes = diction.keys()

def main():
    host = "127.0.0.1"
    port = 2233
    s = socket.socket()
    s.bind((host, port))
    s.listen(10)
    print("Server Started")
    print(keyes)
    while True:
        conn, addr = s.accept()
        conn.send("Welcome to the server.\nEnter MARK-ATTENDANCE followed by the ROLLNUMBER".encode())
        Thread(target = mark, args=(conn, addr)).start()
    s.close()

def mark(c, a):
    dic = {}
    while True:
        try:
            data = c.recv(2048).decode()
            print(data)
            parse = str(data).split(" ")
            if(len(parse) == 2):
                if parse[0] == "MARK-ATTENDANCE":
                    if parse[1] in keyes:
                        dic[c] = parse[1]
                        c.send(("SECRETQUESTION " + diction[parse[1]][0]).encode())
                    else:
                        c.send("ROLLNUMBER-NOTFOUND".encode())
                        break
                elif parse[0] == "SECRETANSWER":
                    if parse[1] == diction[dic[c]][1]:
                        c.send("ATTENDANCE-SUCCESS".encode())
                        break
                    else:
                        c.send(("ATTENDANCE FAILURE\nSECRETQUESTION " + diction[dic[c]][0]).encode())
            else:
                c.send("Invalid-Syntax".encode())
        except:
            continue
    c.close()

if __name__ == '__main__':
    main()