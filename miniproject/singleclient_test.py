# Include Python's Socket Library
from socket import *
import time

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

for i in range(len(sentence)):
    # Connect to TCP Server Socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    print('----------------------------------------------------------------------')
    print('Test ' + str(i+1) + ', Expected code: ' + str(sentence[i][0]) + ', Message: ' + sentence[i][1])
    # Send! No need to specify Server Name and Server Port! Why?
    if i == 9:
        time.sleep(10)
        clientSocket.send(sentence[i][1].encode())
    else:
        clientSocket.send(sentence[i][1].encode())

    # Read reply characters! No need to read address! Why?
    modifiedSentence = clientSocket.recv(1024)

    # Print out the received string
    print ('From Server:', modifiedSentence.decode())
    print('----------------------------------------------------------------------')

    # Close the socket
    clientSocket.close()
    time.sleep(1)
