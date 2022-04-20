from socket import *
import threading
import os
import struct
import os.path
import datetime
import time
import select

def Server(connectionSocket, addr, thread_timeout):
    print('Waiting for the connection：' + str(addr))
    code = '0'
    version1_0 = ['GET', 'POST', 'HEAD']
    version1_1 = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'PATCH', 'CONNECT', 'TRACE', 'OPTIONS']
    folder = os.getcwd()
    pattern = '%d %m %Y %H:%M:%S '
    try:
        # Read from socket (but not address as in UDP)
        sentence = connectionSocket.recv(1024).decode('utf-8')
    except Exception:  # connectionSocket.timeout:
        code = '408'
        version = '?'
        print('timeout')

    if code != '408':
        request_header = sentence.split('\r\n')
        request_line = request_header[0].split(' ')
        # print(request_line)
        header_elements = []

        # Get request header elements
        for headers in request_header:
            header_element = headers.split(': ')
            header_elements.append(header_element[0])
            if header_element[0] == 'If-Modified-Since':
                since = header_element[1]

        # print(header_elements)

        # request_line[0] = method, request_line[1] = resource, request_line[2] = version
        # Check syntax and extract method, filename and version
        if len(request_line) != 3:
            code = '400'
            version = '?'
        else:
            code = '200'
            method = request_line[0]
            if len(request_line[1]) < 2 or request_line[1][0] != '/':
                code = '400'
            else:
                filename = request_line[1][1:]
            if len(request_line[2]) < 6 or request_line[2][0:5] != 'HTTP/':
                code = '400'
            else:
                version = request_line[2][5:]

    # Check HTTP version and method validation
    if code == '200' and version == '1.0':
        if method in version1_0:
            code = '200'
        else:
            code = '400'
    elif code == '200' and (version == '1.1' or version == '2'):
        if method in version1_1:
            code = '200'
        else:
            code = '400'
    else:
        if code == '200':
            code = '400'

    valid_file = 0

    if code == '200':
        for file in os.listdir(folder):
            if file == filename:
                valid_file = 1
        if valid_file == 0:
            code = '404'

    if code == '200' and 'If-Modified-Since' in header_elements:
        try:
            time_info = since.split(', ')[1]
            time_info = time_info.split(' ')
            time_info[1] = str(datetime.datetime.strptime(time_info[1], '%b').month)
            time_info_s = ''
            for i in range(len(time_info) - 1):
                time_info_s = time_info_s + time_info[i] + ' '
            t_in_time = time.strptime(time_info_s, pattern)
            since = time.mktime(t_in_time)
            mtime = os.path.getmtime(filename)
            #print(mtime)
            #print(since)
            if mtime < since:
                code = '304'
        except Exception:
            code = '400'

    print(code)

    # creating object(resource) file
    if code == '200':
        file = open(filename, 'rb')
        read = file.read()
        file.close()
        length_read = len(read)
        format_read = str(length_read) + 's'

    # creating status line
    if code == '200':
        status_line = bytes(("HTTP/" + version + " " + code + " OK\r\n\r\n"), 'utf-8')
        length_status = len(status_line)
        format_status = str(length_status) + 's'
    elif code == '304':
        status_line = bytes(("HTTP/" + version + " " + code + " Not Modified\r\n"), 'utf-8')
        length_status = len(status_line)
        format_status = str(length_status) + 's'
    elif code == '400':
        status_line = bytes(("HTTP/" + version + " " + code + " Bad Request\r\n"), 'utf-8')
        length_status = len(status_line)
        format_status = str(length_status) + 's'
    elif code == '404':
        status_line = bytes(("HTTP/" + version + " " + code + " Not Found\r\n"), 'utf-8')
        length_status = len(status_line)
        format_status = str(length_status) + 's'
    elif code == '408':
        status_line = bytes(("HTTP/" + version + " " + code + " Request Timeout\r\n"), 'utf-8')
        length_status = len(status_line)
        format_status = str(length_status) + 's'

    # format for pack function and creating response to send
    if code == '200':
        formating = format_status + format_read
        response = struct.pack(formating, status_line, read)
    else:
        formating = format_status
        response = struct.pack(formating, status_line)

    # print(response)

    # send response to client
    connectionSocket.send(response)

    if code == '408':
        # Close connection to client (but not welcoming socket)
        connectionSocket.shutdown(1)
        time.sleep(thread_timeout)
        #connectionSocket.close()
    else:
        connectionSocket.close()


if __name__ == '__main__':

    threads = []

    # Specify Server Port
    serverPort = 12000
    # Thread life time if needed
    thread_timeout = 30
    # Create TCP welcoming socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Bind the server port to the socket
    serverSocket.bind(('', serverPort))
    # Server begins listerning foor incoming TCP connections
    serverSocket.listen(5)
    print('The server is ready to receive')

    while True:
        # New socket created on return
        connectionSocket, addr = serverSocket.accept()
        print("connected by", addr)
        connectionSocket.settimeout(5)

        newServerThread = threading.Thread(target=Server, args=(connectionSocket, addr, thread_timeout))
        newServerThread.start()
        threads.append(newServerThread)
        #for t in threads:
        #    t.join()
        #print("Exiting Main Thread")
        #print(threads)
        
        
    serverSocket.close()
