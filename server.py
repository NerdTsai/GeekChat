# -*- coding: utf-8 -*-
import threading
import socket
import sys

server_ip = raw_input("input this server's ip adrress: ")
port = 2345
data = ''
conlock = threading.Condition()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
sock.bind((server_ip,port))
sock.listen(50)
print 'Socket now listening'

def TranData(s):
	global data
	if conlock.acquire():
		data = s
		conlock.notifyAll()
		conlock.release()

def ClientIn(client):
	global data
	try:
		temp = client.recv(4096)
		TranData(temp)
		print data
	except:
		TranData(nick + " leaves the room!")
		print data

def ClientOut(client):
	global data
	while True:
		if conlock.acquire():
			conlock.wait()
			if data:
				try:
					client.send(data)
					conlock.release()
				except:
					conlock.release()
					return

while True:
	client,addr = sock.accept()
	nick = client.recv(1024)
	print str((threading.activeCount()+1)/2) + ' person Online!'
	client.send(data)
	threading.Thread(target = ClientIn , args = (client,)).start()
	threading.Thread(target = ClientOut , args = (client,)).start()
