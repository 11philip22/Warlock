import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("socket created")

try:
	s.bind(("127.0.0.1",4444))
except socket.error as msg:
	print(msg)
	exit()

print("Socket bind complete")

s.listen()
print("socket now listening")

while True:
	conn, addr = s.accept()
	print("Connected with "+addr[0]+":"+str(addr[1]))
	conn.send(b"moi eem")