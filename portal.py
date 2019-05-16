#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import threading
import os
import libtmux
import time
import shutil
import getopt

class transrecieve:
	#connect the stdin and stdout of the sockets
	def stuur(self, conn, unix_conn):
		try:
			while True:
				conn.send(unix_conn.recv(1024))
		except:
			exterminatus()
	
	def ontvang(self, conn, unix_conn):
		try:
			while True:
				unix_conn.send(conn.recv(1024))
		except:
			exterminatus()

class Socket_Server:
	def __init__(self, port=4444 ,addres="127.0.0.1"):
		self.addres=addres
		self.port=port

	def shell(self, conn, addr, locatie):
		# create a new unix sock
		unix_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

		#make folder inside the main folder for this connection
		if not os.path.exists("{0}/{1}".format(locatie, addr[0])):
			os.makedirs("{0}/{1}".format(locatie, addr[0]))
		
		#bind the unix socket
		unix_sock.bind("{0}/{1}/{2}.s".format(locatie, addr[0], addr[1]))
		unix_sock.listen()
		
		#connect ncat to the unix socket
		ncat = "ncat -U /{0}/{1}/{2}.s".format(locatie, addr[0], addr[1])

		#start a tmux session
		# TODO: check if there is a tmux session running named netcat instead of checking if the tmux socket
		if not os.path.exists("{0}/tmux".format(locatie)):
		# if not os.system("tmux -S {0}/tmux ls".format(locatie)) == 0: 
			os.system("tmux -S {0}/tmux new -s netcat -d".format(locatie))
			os.system("tmux -S {0}/tmux send-keys -t netcat.0 \"{1}\" ENTER".format(locatie, ncat))
			print("you can now connect to: {0}/tmux using tmux -S".format(locatie))
		else:
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
			stuurthread = threading.Thread(target=self.stuur, args=(conn, unix_conn))
			ontvangthread = threading.Thread(target=self.ontvang, args=(conn, unix_conn))
			stuurthread.start()
			ontvangthread.start()
		
	def exterminatus(self):
		#remove socket if no longer used WIP
		print("{0}:{1}".format(addr[0], addr[1]))
		os.remove("{0}/{1}/{2}.s".format(locatie, addr[0], addr[1]))
		#remove underlaying folder if empty
		if not os.listdir("{0}/{1}".format(locatie, addr[0])):
			os.rmdir("{0}/{1}".format(locatie, addr[0]))

	def engage(self):
		locatie = "/tmp/warlock"
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print("starting the server on: {0}:{1}".format(addres, port))
		print("socket created")

		try:
			s.bind((self.addres, self.port))
		except socket.error as msg:
			print(msg)
			exit()

		print("Socket bind complete")

		s.listen()
		print("socket now listening")

		#start a thread for for each incomming connection4
		try:
			while True:
				conn, addr = s.accept()
				print("Connected with "+addr[0]+":"+str(addr[1]))
				thread = threading.Thread(target=self.shell, args=(conn, addr, locatie))
				thread.daemon = True
				thread.start()
		except KeyboardInterrupt:
			#clean up all the files if program closes
			if os.path.exists(locatie):
				shutil.rmtree(locatie)
			#very dirty workaround disable this if you use tmux for other stuff
			os.system("kill $(pgrep tmux)")
			print("bye bye")

port = int(sys.argv[1])

if len(sys.argv) > 2:
	addres = str(sys.argv[2])
else:
	addres = "127.0.0.1"

ss = Socket_Server(addres=addres, port=port)
ss.engage()

# try:
# 	opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["port=","addres="])
# except getopt.GetoptError:
# 	print("test.py -p <port> -a <addres>")
# 	sys.exit(2)
# for opt, arg in opts:
# 	if opt == "-h":
# 		print("test.py -p <port> -a <addres>")
# 		sys.exit()
# 	elif opt in ("-p", "--port"):
# 		port = arg
# 	elif opt in ("-a", "--addres"):
# 		addres = arg
# try:
# 	ss = Socket_Server(addres=addres, port=port)
# 	ss.engage()
# except:
# 	ss = Socket_Server()
# 	ss.engage()