#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Para que entienda acentos

import socket
import sys
from _thread import *

SERVER_ADDR = ''
SERVER_PORT = 5555
SERVER_PORT_LISTENING_FOR_SERVER_1 = 6666
SERVER_PORT_LISTENING_FOR_SERVER_2 = 7777

# CREATE SOCKET VAR OF TYPE TCP TO LISTE FOR CLIENT CONNECTION
sListeningClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# CREATE SOCKET VAR OF TYPE TCP TO LISTEN FOR SERVER 1 CONNECTION
sListeningServer1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# CREATE SOCKET VAR OF TYPE TCP TO LISTEN FOR SERVER 2 CONNECTION
sListeningServer2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

# BIND SOCKET FOR LISTENING TO CLIENT CONNECTION TO PORT 5555
try:
	sListeningClient.bind((SERVER_ADDR, SERVER_PORT))
except socket.error as e:
	print("Binding failed: sListeningClient", e)
	sys.exit()
print("Socket has been bounded: sListeningClient")

# BIND SOCKET FOR LISTENING TO SERVER1 CONNECTION TO PORT 6666
try:
	sListeningServer1.bind((SERVER_ADDR, SERVER_PORT_LISTENING_FOR_SERVER_1))
except socket.error as e:
	print("Binding failed: sListeningServer1", e)
	sys.exit()
print("Socket has been bounded: sListeningServer1")

# BIND SOCKET FOR LISTENING TO SERVER2 CONNECTION TO PORT 7777
try:
	sListeningServer2.bind((SERVER_ADDR, SERVER_PORT_LISTENING_FOR_SERVER_2))
except socket.error as e:
	print("Binding failed: sListeningServer2", e)
	sys.exit()
print("Socket has been bounded: sListeningServer2")


sListeningClient.listen(1)
sListeningServer1.listen(1)
sListeningServer2.listen(1)
print("Socket is ready")

# WAIT FOR SERVER1 TO CONNECT AND ACCEPT CONNECTION
connServer1, addrServer1 = sListeningServer1.accept()
print("Nueva conección de servidor:", connServer1.getpeername()[0], connServer1.getpeername()[1])

# WAIT FOR SERVER2 TO CONNECT AND ACCEPT CONNECTION
connServer2, addrServer2 = sListeningServer2.accept()
print("Nueva conección de servidor:", connServer2.getpeername()[0], connServer2.getpeername()[1])

def serverThread(conn):
	print("Thread started", conn.getpeername()[0])

start_new_thread(serverThread, (connServer1,))
start_new_thread(serverThread, (connServer2,))

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
