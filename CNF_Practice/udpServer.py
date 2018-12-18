import socket

def main():
	host = "127.0.0.1"	
	port = 2222

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host,port))

	while True:
		data, adr = s.recvfrom(1024)
		print("Connection Established with: " + str(adr))
		# if not data:
		# 	break
		print ("Data from user: " + str(data.decode()))
		data = str(data.decode()).upper()
		print("Sending data: " + data)
		s.sendto(data.encode(), adr)
	s.close()

if __name__ == '__main__':
	main()