import socket
import sys
import os

def download(module):
	if not os.path.exists("./modules"):
		os.makedir("./modules")

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
home = ('localhost', 10000)
print("connecting to {0} port {1}".format(server_address[0], server_address[1])
sock.connect(home)