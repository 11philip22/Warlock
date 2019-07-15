import threading
import socket

def server():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print("starting the server on: {0}:{1}".format(addres, port))
	s.bind((self.addres, self.port))
	print("Socket bind complete")
	s.listen()
	print("server ready")

	while True:
		conn, addr = s.accept()
		print("Connected with "+addr[0]+":"+str(addr[1]))
		thread = threading.Thread(target=ding args=())
		thread.daemon = True
		thread.start()

