# Include Python's Socket Library
from socket import *
import time
import datetime

# Specify Server Address
serverName = 'localhost'
serverPort = 12000

# Create TCP Socket for Client
clientSocket = socket(AF_INET, SOCK_STREAM)

sentence = []

# TEST 200 code
sentence.append([200,'GET /test.html HTTP/1.1\r\n\r\n'])
# TEST 304 code (induces code 200)
sentence.append([200,'GET /test.html HTTP/1.1\r\nIf-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT\r\n\r\n'])
# TEST 304 code 
sentence.append([304,'GET /test.html HTTP/1.1\r\nIf-Modified-Since: Mon, 08 Apr 2021 07:28:00 GMT\r\n\r\n'])
# TEST 400 code with lack of request elements
sentence.append([400,'/test.html /1.1\r\n\r\n'])
# TEST 400 code with method name
sentence.append([400,'GT /test.html HTTP/1.1\r\n\r\n'])
# TEST 400 code without '/' before the filename
sentence.append([400,'GET test.html HTTP/1.1\r\n\r\n'])
# TEST 400 code with version
sentence.append([400,'GET /test.html HTTP/1.3\r\n\r\n'])
# TEST 400 code with method + version match
sentence.append([400,'PUT /test.html HTTP/1.0\r\n\r\n'])
# TEST 404 code
sentence.append([404,'GET /tst.html HTTP/1.1\r\n\r\n'])
# TEST 408 code
sentence.append([408,'GET /test.html HTTP/1.1\r\n\r\n'])

for i in range(2):
    # Connect to TCP Server Socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    print('----------------------------------------------------------------------')
    print('connected to server: ' + str(datetime.datetime.now()))
    # Send! No need to specify Server Name and Server Port! Why?
    if i == 0:
        for i in range(10):
            time.sleep(1)
            print(str(i+1))
        clientSocket.send(sentence[9][1].encode())
        print('Request sent')
    else:
        clientSocket.send(sentence[2][1].encode())
        print('Request sent')
    
    # Read reply characters! No need to read address! Why?
    modifiedSentence = clientSocket.recv(1024)

    # Print out the received string
    print ('From Server:', modifiedSentence.decode())
    print('----------------------------------------------------------------------')

    # Close the socket
    clientSocket.close()
    time.sleep(1)
