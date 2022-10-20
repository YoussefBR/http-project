import socket
import re
import os
import pdb

SUCCESS_HEADER_SIZE = 15
# Persistant HTTP Server
class InvalidRequest(Exception):
    pass
class LiRequest(Exception):
    pass

def liConvert():
    # Update FILE_LIST before sending
    FILE_LIST = os.listdir("webpages/")
    # Convert to string to send over TCP
    string = "Available files:\n"
    for file in FILE_LIST:
        string = string + (str(file)) + "\n"
    return string

def handleRequest(conn):
    try:
        req = conn.recv(1024).decode()
        # To see the request in terminal
        print("Client sent: " + req)
        # use re to process the request and get string past "GET " until space or end of in
        match = re.search(r'http://', req)
        if(match == None):
            raise InvalidRequest
        # Move to filename location in the request
        start = match.end(0)
        match = re.search(r"/", req[start:])
        # Set the start of the file name
        start = match.end(0) + start
        match = re.search(r'(\.html)', req)
        # Check if a list request
        if(req[start:start+2] == "li"):
            raise LiRequest
        # Check if invalid request
        elif(match is None):
            raise InvalidRequest

        fileName = req[start:match.end(0)]
        print(fileName)
        # try to open file with that name in binary mode
        reqFile = open("webpages/" + fileName, "rb")
        conn.send(("HTTP/1.1 200 OK").encode() + reqFile.read(1024 - SUCCESS_HEADER_SIZE))
        data = reqFile.read(1024)
        while(data):
            conn.send(data)
            data = reqFile.read(1024)
        return True
        # on success start sending file, on fail send back error 404
    except InvalidRequest: 
        conn.send(("Error: Invalid request, try again\n").encode())
    except FileNotFoundError:
        # on file foes not exist this will be returned.
        conn.send(("Error 404: File not found\n").encode())
    except LiRequest:
        conn.send(liConvert().encode())
    return False


HOST = "127.0.0.1"
PORT = 6043
FILE_LIST = os.listdir("webpages/")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
print("Server successfully created")

sock.listen() # param can be inserted here to cap the amount of queued connections while server is busy

while True: # Opportunity to beef this up by adding a pass function to create a personal socket for that request
    conn, address = sock.accept()
    print('Connection from ' + address[0] + ', port #: ' + str(address[1]))

    # Handle http request and return the proper file
    ret = True
    closed = False
    ret = handleRequest(conn)
    while(ret is False):
        try:
            ret = handleRequest(conn)
        except:
            ret = True
            closed = True

    # close the conection and move on
    if(closed is False):
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
    





