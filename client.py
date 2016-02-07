# -*- coding: utf-8 -*-
import threading
import socket

recv_words = ''
send_words = ''

def HandleIn(s):
	global recv_words
	while True:
		try:
			recv_words = s.recv(4096)
			if not recv_words:
				break
			if recv_words != send_words:
				print recv_words
		except:
			break

def HandleOut(s):
	global send_words,nick
	while True:
		send_words = raw_input('>>')
		send_words = nick + ':' + send_words + '\n'
		s.sendall(send_words)

nick = raw_input('input your nickname:')
target_ip = raw_input("input target's ip:")
port = 2345
try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((target_ip , port))
	sock.send(nick)
	print '-------------------Socket created-------------------'
except:
	print "服务器正在重启..."

threading.Thread(target = HandleIn,args = (sock,)).start()
threading.Thread(target = HandleOut,args = (sock,)).start()
