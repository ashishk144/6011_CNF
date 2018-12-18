import socket

def main():
	host = "127.0.0.1"
	port = 1234

	s = socket.socket()
	s.connect((host, port))
	inp = input("Type in the following format \n(value) INR to USD\n")
	while inp != "q":
		s.send(inp.encode())
		data = s.recv(2048)
		print("Converted Value: " + str(data.decode()))
		inp = input("Type: ")
	s.close()

if __name__ == '__main__':
	main()