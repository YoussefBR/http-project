import socket
import sys

SERVER_PORT = 6043

CLIENT_PORT_1 = 4000
SUCCESS_HEADER_SIZE = 15
HOST = '127.0.0.1'

def createReq(request, clientSock):
        # So we know later if we need to print file names or if we need to create a file to get the requested file
        if request == "li":
            li = True
        else:
            li = False
        if request == "exit":
            return True

        # Create the request
        request = "GET " + "http://" + HOST + ":" +  str(SERVER_PORT) + "/" + request + " " + "HTTP/1.1"
        print("Your request:" + request)

        # Send the request
        clientSock.send(request.encode())

        # Handle the response
        response = clientSock.recv(1024)
        if(response.decode()[0:5] != "Error"):
            # list handling
            if(li is True):
                print(response.decode())
                return False
            # file handling
            else:
                newFile = open("requestedFile.html", "wb")
                response = response[SUCCESS_HEADER_SIZE: ]
                print("Receiving file.")
                while(response):
                    newFile.write(response)
                    response = clientSock.recv(1024)
                print("File received.")
                newFile.close()
        # error handling
        else:
            print(response.decode())
            return False
        return True
        


clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.bind((HOST, CLIENT_PORT_1))


try:
    clientSock.connect((HOST, SERVER_PORT))
except:
    print("Connection failed try running Client again")
    sys.exit()
print("Successfully connected.")

done = False
while(done is False):
    uIn = str(input("Welcome. Please enter the name of the file you'd like. You may also enter 'li' to see a list of all currently available files or 'exit' to end the connection: \n"))
    done = createReq(uIn, clientSock)
clientSock.close()
print("Connection ended.")


        


