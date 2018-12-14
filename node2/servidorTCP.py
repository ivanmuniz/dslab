#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Para que entienda acentos

import socket
import sys
from _thread import *

# FOR CLIENT CONNECTION
SERVER_ADDR = ''
SERVER_PORT = 5555
SERVER_PORT_LISTENING_FOR_SERVER_1 = 6666

# FOR THIS SERVER TO CONNECT WITH THE 3rd SERVER
SERVER3_ADDR = ''
SERVER3_PORT = 7777

sListeningClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sListeningServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sConnectServer3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

try:
	sListeningClient.bind((SERVER_ADDR, SERVER_PORT))
except socket.error as e:
	print("Binding failed: sListeningClient", e)
	sys.exit()
print("Socket has been bounded: sListeningClient")

try:
	sListeningServer.bind((SERVER_ADDR, SERVER_PORT_LISTENING_FOR_SERVER_1))
except socket.error as e:
	print("Binding failed: sListeningServer", e)
	sys.exit()
print("Socket has been bounded: sListeningServer")

try:
	sConnectServer3.connect((SERVER3_ADDR, SERVER3_PORT))
except socket.error as e:
	print("Connection to server 3 failed: sConnectServer3", e)
	sys.exit()
print("Connection with 3rd server successfull: sConnectServer3")

sListeningClient.listen(10)
sListeningServer.listen(10)
print("Socket is ready")

# ACEPTA LA CONECCIÓN DEL SERVIDOR 1 Y GUARDA LOS DATOS DE LA CONECCIÓN
connServer1, addrServer1 = sListeningServer.accept()
print("Nueva conección de servidor:", connServer1.getpeername()[0], connServer1.getpeername()[1])

def serverThread(conn):
	print("Thread started", conn.getpeername()[0])

start_new_thread(serverThread, (connServer1,))
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
