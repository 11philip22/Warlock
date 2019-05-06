#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import threading

def shell(conn):
	stuurthread = threading.Thread(target=stuur, args=(conn,))
	ontvangthread = threading.Thread(target=ontvang, args=(conn,))
	stuurthread.start()
	ontvangthread.start()

def stuur(conn):
	while True:
		cmd = input()
		conn.send(bytes(cmd+"\n", encoding="utf-8"))

def ontvang(conn):
	while True:
		recieved = conn.recv(255)
		print(recieved.decode('utf-8'))

addres = "127.0.0.1"
port = int(sys.argv[1])

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("socket created")

try:
	s.bind((addres,port))
except socket.error as msg:
	print(msg)
	exit()

print("Socket bind complete")

s.listen()
print("socket now listening")

while True:
	conn, addr = s.accept()
	print("Connected with "+addr[0]+":"+str(addr[1]))
	thread = threading.Thread(target=shell, args=(conn,))
	thread.start()
