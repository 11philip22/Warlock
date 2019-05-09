#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import threading
import os
import libtmux
import time
import shutil

def shell(conn, addr, locatie):
	# create a new unix sock
	unix_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

	#make folder inside the main folder for this connection
	if not os.path.exists("{0}/{1}".format(locatie, addr[0])):
		os.makedirs("{0}/{1}".format(locatie, addr[0]))
	
	#bind the unix socket
	unix_sock.bind("{0}/{1}/{2}.s".format(locatie, addr[0], addr[1]))
	unix_sock.listen()
	
	#start a tmux session
	if not os.path.exists("{0}/tmux".format(locatie)):
		os.system("tmux -S {0}/tmux new -s netcat -d".format(locatie))

	#connect to the socket
	ncat = "ncat -U /{0}/{1}/{2}.s".format(locatie, addr[0], addr[1])
	#make a new tmux window for this connection
	tmux = libtmux.Server("", "{0}/tmux".format(locatie))
	time.sleep(1)
	tmux_session = tmux.find_where({ "session_name": "netcat" })
	window = tmux_session.new_window(attach=False)
	pane = window.select_pane(1)
	pane.send_keys(ncat)

	#connect the unix socket to the tcp socket
	while True:
		unix_conn, unix_addr = unix_sock.accept()
		stuurthread = threading.Thread(target=stuur, args=(conn, unix_conn))
		ontvangthread = threading.Thread(target=ontvang, args=(conn, unix_conn))
		stuurthread.start()
		ontvangthread.start()

#connect the stdin and stdout of the sockets
def stuur(conn, unix_conn):
	while True:
		conn.send(unix_conn.recv(1024))

def ontvang(conn, unix_conn):
	while True:
		unix_conn.send(conn.recv(1024))

locatie = "/tmp/warlock"
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

#start a thread for for each incomming connection
try:
	while True:
		conn, addr = s.accept()
		print("Connected with "+addr[0]+":"+str(addr[1]))
		thread = threading.Thread(target=shell, args=(conn, addr, locatie))
		thread.daemon = True
		thread.start()
except KeyboardInterrupt:
	shutil.rmtree(locatie)
	print("bye bye")