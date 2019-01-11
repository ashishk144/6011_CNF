import socket

def main():
	host = "127.0.0.1"
	port = 2333
	server = ("127.0.0.1", 2222)
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host, port))
	inp = input("Type: ")
	while True:
		s.sendto(inp.encode(), server)
		data, adr = s.recvfrom(2048)
		print("Received from: " + str(adr))
		print("Message: " + str(data.decode()))
		inp = input("Type: ")
	s.close()

if __name__ == '__main__':
	main()