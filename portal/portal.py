#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import threading
import os
import libtmux
import time
import shutil


def socketserver(addres, port, max_connections, locatie):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("starting the server on: {0}:{1}".format(addres, port))

    try:
        s.bind((addres, port))
    except socket.error as msg:
        print(msg)
        exit()

    s.listen(max_connections)

    try:
        while True:
            conn, addr = s.accept()
            w = Worker(port=port, locatie=locatie, addr=addr, conn=conn)
            print("Connected with "+addr[0]+":"+str(addr[1]))
            thread = threading.Thread(target=w.start)
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        if os.path.exists(locatie):
            shutil.rmtree(locatie)


class Worker:
    def __init__(self, port, locatie, addr, conn):
        self.port = port
        self.locatie = locatie
        self.addr = addr
        self.conn = conn
        self.unix_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def start(self):
        self.unix_socket()
        self.tmux()
        self.connection()

    def unix_socket(self):
        if not os.path.exists("{0}/{1}".format(self.locatie, self.addr[0])):
            os.makedirs("{0}/{1}".format(self.locatie, self.addr[0]))

        self.unix_sock.bind("{0}/{1}/{2}.s".format(self.locatie,
                                                   self.addr[0],
                                                   self.addr[1]))
        self.unix_sock.listen(1)

    def tmux(self):
        ''' tought
        Maybe split tmux with a collum on the left side
        running a iteractive program showing open connections.
        Selecting a connection and pressing enter would
        send apropiate tmux commands to show shell of that session
        on right section of the screen'''
        ncat = "ncat -U /{0}/{1}/{2}.s".format(self.locatie,
                                               self.addr[0],
                                               self.addr[1])
        tmuxcreate = "tmux -S {0}/tmux new -s netcat -d".format(self.locatie)
        tmuxsendkeys = "tmux -S {0}/tmux send-keys -t netcat.0 \
                       \"{1}\" ENTER".format(self.locatie, ncat)

        if not os.path.exists("{0}/tmux".format(self.locatie)):
            os.system(tmuxcreate)
            os.system(tmuxsendkeys)
            print("you can now connect to: {0}/tmux using \"tmux -S\"".format(
                self.locatie))
        else:
            try:
                tmux = libtmux.Server("", "{0}/tmux".format(self.locatie))
                time.sleep(1)
                tmux_session = tmux.find_where({"session_name": "netcat"})
                window = tmux_session.new_window(attach=False)
                pane = window.select_pane(1)
                pane.send_keys(ncat)
            except:
                os.system(tmuxcreate)
                os.system(tmuxsendkeys)

    def connection(self):
        while True:
            unix_conn, unix_addr = self.unix_sock.accept()
            stuurthread = threading.Thread(target=self.stuur,
                                           args=[unix_conn])
            stuurthread.start()
            ontvangthread = threading.Thread(target=self.ontvang,
                                             args=[unix_conn])
            ontvangthread.start()

    def stuur(self, unix_conn):
        try:
            while True:
                self.conn.send(unix_conn.recv(1024))
        except socket.error:
            self.exterminatus()

    def ontvang(self, unix_conn):
        try:
            while True:
                unix_conn.send(self.conn.recv(1024))
        except socket.error:
            self.exterminatus()

    def exterminatus(self):
        # remove socket is no longer used WIP
        print("{0}:{1}".format(self.addr[0], self.addr[1]))
        # why doesnt os.remove work ???
        # os.remove("{0}/{1}/{2}.s".format(self.locatie,
        #                                  self.addr[0],
        #                                  self.addr[1]))
        os.system("rm {0}/{1}/{2}.s".format(self.locatie,
                                            self.addr[0],
                                            self.addr[1]))
        # remove underlaying folder if empty
        if not os.listdir("{0}/{1}".format(self.locatie, self.addr[0])):
            # os.rmdir("{0}/{1}".format(self.locatie, self.addr[0]))
            os.system("rmdir {0}/{1}".format(self.locatie, self.addr[0]))

        # self.window.kill_window()
        # maybe give tmux windows a name and delete by name


if __name__ == '__main__':
    ''' todo
    better argparsing'''
    port = int(sys.argv[1])
    addres = "127.0.0.1"
    max_connections = 100
    locatie = "/tmp/warlock"
    socketserver(addres, port, max_connections, locatie)
