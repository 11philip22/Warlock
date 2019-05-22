#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import threading
import os
import libtmux
import time
import shutil

def socketserver(addres, port):
	locatie = "/tmp/warlock"

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print("starting the server on: {0}:{1}".format(addres, port))
	
	try:
		s.bind((addres, port))
	except socket.error as msg:
		print(msg)
		exit()

	s.listen()

	try:
		while True:
			conn, addr = s.accept()
			w = Worker(port=port, locatie=locatie, addr=addr, conn=conn)
			print("Connected with "+addr[0]+":"+str(addr[1]))
			thread = threading.Thread(target=w.start())
			thread.daemon = True
			thread.start()
	except KeyboardInterrupt:
		if os.path.exists(locatie):
			shutil.rmtree(locatie)

class Worker:
	def __init__(self, port, locatie, addr, conn):
		self.addres = addres
		self.port = port
		self.locatie = locatie
		self.addr = addr
		self.conn = conn

	def start(self):
		self.unix_socket()
		self.connection()
		self.tmux()

	def unix_socket(self):
		if not os.path.exists("{0}/{1}".format(self.locatie, self.addr[0])):
			os.makedirs("{0}/{1}".format(self.locatie, self.addr[0]))

		self.unix_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.unix_sock.bind("{0}/{1}/{2}.s".format(self.locatie, self.addr[0], self.addr[1]))
		self.unix_sock.listen()
		
	def tmux(self):
		ncat = "ncat -U /{0}/{1}/{2}.s".format(self.locatie, self.addr[0], self.addr[1])
		
		if not os.path.exists("{0}/tmux".format(self.locatie)):
			os.system("tmux -S {0}/tmux new -s netcat -d".format(self.locatie))
			os.system("tmux -S {0}/tmux send-keys -t netcat.0 \"{1}\" ENTER".format(self.locatie, ncat))
			print("you can now connect to: {0}/tmux using tmux -S".format(self.locatie))
		else:
			tmux = libtmux.Server("", "{0}/tmux".format(self.locatie))
			time.sleep(1)
			tmux_session = tmux.find_where({ "session_name": "netcat" })
			window = tmux_session.new_window(attach=False)
			pane = window.select_pane(1)
			pane.send_keys(ncat)

	def connection(self):
		while True:
			unix_conn, unix_addr = self.unix_sock.accept()
			stuurthread = threading.Thread(target=self.stuur(self.conn, unix_conn))
			stuurthread.start()
			ontvangthread = threading.Thread(target=self.ontvang(self.conn, unix_conn))
			ontvangthread.start()

	def stuur(self, unix_conn):
		try:
			while True:
				self.conn.send(unix_conn.recv(1024))
		except:
			self.exterminatus()
			# print("oepsie stuur")

	def ontvang(self, conn, unix_conn):
		try:
			while True:
				unix_conn.send(self.conn.recv(1024))
		except:
			self.exterminatus()
			# print("oepsie ontvang")

	def exterminatus(self):
		#remove socket if no longer used WIP
		print("{0}:{1}".format(self.addr[0], self.addr[1]))
		os.remove("{0}/{1}/{2}.s".format(self.locatie, self.addr[0], self.addr[1]))
		#remove underlaying folder if empty
		if not os.listdir("{0}/{1}".format(self.locatie, self.addr[0])):
			os.rmdir("{0}/{1}".format(self.locatie, self.addr[0]))

if __name__ == '__main__':
	port = int(sys.argv[1])

	if len(sys.argv) > 2:
		addres = str(sys.argv[2])
	else:
		addres = "127.0.0.1"

	socketserver(addres, port)