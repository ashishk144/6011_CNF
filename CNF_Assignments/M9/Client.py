import socket

def main():
	s = socket.socket()
	host = "127.0.0.1"
	port = 5128
	s.connect((host, port))
	data = s.recv(2048)
	print(data.decode())
	while True:
		inp = input("Enter the guess between 1 and 50")
		s.send(inp.encode())	
		data = s.recv(2048).decode()
		if not data:
			break
		print(data)
		check = str(data).split(" ")
		if check[4] == "correct" or check[4] == "max":
			break
	s.close()

if __name__ == '__main__':
	main()