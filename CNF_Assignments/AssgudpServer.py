import socket

def main():
    host = "127.0.0.1"  
    port = 2222

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    diction = {"USD": 1, "INR":67, "Pounds": 0.75, "Yen": 113.41}

    while True:
        data, adr = s.recvfrom(1024)
        print("Connection Established with: " + str(adr))
        if not data:
            break
        print ("Data from user: " + str(data.decode()))
        data = str(data.decode()).split(" ")
        value = int(data[0]) * (diction[data[3]]/diction[data[1]])
        print("Sending data: " + str(value))
        data = str(value)
        s.sendto(data.encode(), adr)
    s.close()

if __name__ == '__main__':
    main()