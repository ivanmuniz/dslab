#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Para que entienda acentos

import socket
import sys

SERVER_URL = 'localhost'
SERVER_PORT = 5555

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print("Failed to connect")
	sys.exit()
print("Socket Created")

# TO GET IP OF THE HOST BY GIVING IT A URL
try:
	SERVER_IP = socket.gethostbyname(SERVER_URL)
except socket.gaierror:
	print("Hostname could not be resolved")
	sys.exit()

try:
	s.connect((SERVER_IP, SERVER_PORT))
except socket.error as e:
	print("Error connecting to server:", e)
	sys.exit()


print("Socket Connected to " + SERVER_URL + " using IP " + SERVER_IP)
welcomeMessage = s.recv(1024)
print(welcomeMessage.decode())

while 1:
	message = input("Mensaje: ")
	if message != "salir":
		try:
			s.sendall(message.encode())
		except socket.error:
			print("Did not send successfully")
			sys.exit()
		reply = s.recv(1024)
		print(reply.decode())
	else:
		break

s.shutdown(1)
s.close()