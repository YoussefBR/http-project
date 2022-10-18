import socket

SERVER_PORT = 6043

CLIENT_PORT_1 = 4000
HOST = '127.0.0.1'

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock1.bind((HOST, CLIENT_PORT_1))
except socket.error as error:
    print('Error ' + error[0] + ': ' + error[1])
else: 
    print('Socket 1 successfully created');

sock1.connect((HOST, SERVER_PORT))

