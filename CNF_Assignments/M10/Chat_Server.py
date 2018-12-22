import socket
import os
from threading import *
import time
import signal

def Main():
	host = '127.0.0.1'
	port = 2325
	s = socket.socket()
	s.bind((host,port))
	print('server started: ' + str(os.getpid()))
	s.listen(10)
	clients = []
	names = {}
	while True:
		c, adr = s.accept()
		c.send('Enter your Name folkk!: '.encode())
		conn_name = c.recv(1024)
		print('Connected Users' + conn_name.decode())
		names[c] = str(conn_name.decode())
		clients.append(c)
		for con in clients:
			if c != con:
				con.send((names[c] + ' is Connected.').encode())
		thread = Thread(target = client, args = (c, adr, clients, names)).start()
	s.close()

def kill():
	print(active_count())
	if (active_count() == 2):
		print('Going to Sleep.....')
		time.sleep(10)
		if (active_count() == 2):
			os.kill(os.getpid(), signal.CTRL_BREAK_EVENT)

def client(c, adr, clients, names):
	while True:
		try:
			message = (c.recv(1024)).decode()
			print(names[c] + '<-->' + message)
			if message != 'exit' and c in clients:
				for client in clients:
					if c != client:
						try:
							name = names[c]
							client.send((name + '---->>>' + message).encode())
						except:
							c.close()
							delete(c, clients)
			else:
				c.send(('Do you want to Exit?(Y/N)').encode())
				if ((c.recv(1024)).decode() == 'Y'):
					for con in clients:
						if c != con:
							con.send((names[c] + ' is disconnected. Users online: ' + str(active_count() - 2)).encode())
					c.send('Disconnected'.encode())
					delete(c,clients)
					kill()
					return 1
		except:
			continue
	c.close()
def delete(c, clients):
	if c in clients:
		clients.delete(c)
if __name__ == '__main__':
	Main()