#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Para que entienda acentos

import socket
import sys
from _thread import *

# FOR CLIENT CONNECTION
SERVER_ADDR = ''
SERVER_PORT = 5555
SERVER_PORT_LISTENING_SERVERS = 6666	# SE PUEDE BORRAR YA QUE EL SERVIDOR 1 NO VA A ESCUCHAR
										# CONECCIONES, SÓLO EL SERVIDOR 2 Y 3 VAN A ESCUHAR

# FOR THIS SERVER TO CONNECT WITH THE 2nd SERVER
SERVER2_ADDR = ''
SERVER2_PORT = 6666

# FOR THIS SERVER TO CONNECT WITH THE 3rd SERVER
SERVER3_ADDR = ''
SERVER3_PORT = 6666

sListeningClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sConnectServer2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sConnectServer3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

# try:
# 	sListeningClient.bind((SERVER_ADDR, SERVER_PORT))
# except socket.error as e:
# 	print("Binding failed: sListeningClient", e)
# 	sys.exit()
# print("Socket has been bounded: sListeningClient")


sListeningClient.listen(10)
print("Socket is ready: sListeningClient")

try:
	sConnectServer2.connect((SERVER2_ADDR, SERVER2_PORT))
except socket.error as e:
	print("Connection to server 2 failed: sConnectServer2", e)
	sys.exit()
print("Connection with 2nd server successfull: sConnectServer2")

try:
	sConnectServer3.connect((SERVER3_ADDR, SERVER3_PORT))
except socket.error as e:
	print("Connection to server 3 failed: sConnectServer3", e)
	sys.exit()
print("Connection with 3rd server successfull: sConnectServer3")

def serverThread(conn):
	print("Thread started", conn.getpeername()[0])

start_new_thread(serverThread, (sConnectServer2,))
start_new_thread(serverThread, (sConnectServer3,))

def clientThread(conn):
	message = "Welcome to the server"
	conn.send(message.encode())
	while 1:
		# BLOCKS UNTIL RECEIVES A MSG
		data = conn.recv(1024)
		reply = "OK."
		if not data:
			break
		print(data.decode())
		conn.sendall(reply.encode())
	print("Connection closed with " + str(conn.getpeername()[1]))
	conn.close()


while 1:
	# BLOCKS UNTIL RECEIVES CONNECTION
	conn, addr = sListeningClient.accept()
	print("Connected with " + addr[0] + ":" + str(addr[1]))
	start_new_thread(clientThread, (conn,))


sListeningClient.close()
