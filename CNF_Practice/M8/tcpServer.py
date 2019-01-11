import socket

def main():
	host = "127.0.0.1"	
	port = 1234

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
		data = str(data.decode()).upper()
		print("Sending data: " + data)
		conn.send(data.encode())
	conn.close()

if __name__ == '__main__':
	main()