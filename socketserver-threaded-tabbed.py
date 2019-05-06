#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import threading
import subprocess
import os
import libtmux

def shell(conn, addr):
	unix_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

	if not os.path.exists('/tmp/flipnet/'+addr[0]):
		os.makedirs("/tmp/flipnet/"+addr[0])
	
	unix_sock.bind("/tmp/flipnet/"+addr[0]+"/"+str(addr[1])+".s")
	unix_sock.listen()
	
	if subprocess.call(["tmux -S /tmp/flipnet/tmux ls"], shell=True) == 1:
		subprocess.Popen(["tmux -S /tmp/flipnet/tmux new -s netcat -d"], shell=True)

	ncat = "ncat -U /tmp/flipnet/"+addr[0]+"/"+str(addr[1])+".s"
	tmux = libtmux.Server("", "/tmp/flipnet/tmux")
	tmux_session = tmux.find_where({ "session_name": "netcat" })
	window = tmux_session.new_window(attach=False)
	pane = window.select_pane(1)
	pane.send_keys(ncat)

	while True:
		unix_conn, unix_addr = unix_sock.accept()
		stuurthread = threading.Thread(target=stuur, args=(conn, unix_conn))
		ontvangthread = threading.Thread(target=ontvang, args=(conn, unix_conn))
		stuurthread.start()
		ontvangthread.start()

def stuur(conn, unix_conn):
	while True:
		conn.send(unix_conn.recv(1024))

def ontvang(conn, unix_conn):
	while True:
		unix_conn.send(conn.recv(1024))

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
	thread = threading.Thread(target=shell, args=(conn, addr))
	thread.start()