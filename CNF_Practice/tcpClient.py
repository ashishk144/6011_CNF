import socket

def main():
	host = "127.0.01"
	port = 1234

	s = socket.socket()
	s.connect((host, port))
	inp = input("Type: ")
	while inp != "q":
		s.send(inp.encode())
		data = s.recv(2048)
		print("Received from: " + str(data.decode()))
		inp = input("Type: ")
	s.close()

if __name__ == '__main__':
	main()