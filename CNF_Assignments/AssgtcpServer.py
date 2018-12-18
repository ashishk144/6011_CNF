import socket

def main():
    host = "127.0.0.1"  
    port = 1234
    diction = {"USD": 1, "INR":67, "Pounds": 0.75, "Yen": 113.41}
    s = socket.socket()
    s.bind((host,port))

    s.listen(1)
    conn, adr = s.accept()
    print("Connection Established with: " + str(adr))
    while True:
        data = conn.recv(2048)
        if not data:
            break
        print ("Data from user: " + str(data.decode()))
        data = str(data.decode()).split(" ")
        value = int(data[0]) * (diction[data[3]]/diction[data[1]])
        data = str(value)
        print("Sending data: " + data)
        conn.send(data.encode())
    conn.close()

if __name__ == '__main__':
    main()