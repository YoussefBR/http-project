import socket
import re 

# FOR LATER
# Throw in the parser implementation? Allows this to be a bit better of a resume padder. 
#   Important parser functions:
#       re.findall()
#           when iterating to parse for validness use this and check length of the 

# THIS FILE
# Create the server socket. Diff between socket and http socket?

class Server:

    def __init__(self, database):
        self.database = database
    
    def __enter__(self):
        pass

    def __exit__(self):

        pass

HOST = "127.0.0.1"
PORT = 6043

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.bind((HOST, PORT))
except socket.error as error:
    print('Error ' + error[0] + ': ' + error[1])
else: 
    print('Socket successfully created');

sock.listen() # param can be inserted here to cap the amount of queued connections while server is busy

while True: # Opportunity to beef this up by adding a pass function to create a personal socket for that request
    conn, address = sock.accept()
    print('Connection from ' + address[0] + ', port #: ' + str(address[1]))

    # Handle http request and return the proper file

    # close connection
    conn.close()

    





