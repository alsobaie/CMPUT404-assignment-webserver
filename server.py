#  coding: utf-8 
import socketserver

# to get current date formated for http1.1 response
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

from os import fork # to fork processes
import os.path # to check if file exists

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        payload = ''
        code = ''
        response = ''
        contentType = ''
        uri = 'www'
        
        self.data = self.request.recv(1024).strip().decode()
        #print ("\nGot a request of:\n\n{}".format(self.data))
        data = self.data.split()
        
        method = data[0]
        uri += data[1]
        uriEnd = uri[uri.rfind('/')+1:]
        
        if(not '.' in uriEnd):
            if(uri[-1] != '/'):
                uri += '/'
            uri += 'index.html'
            uriEnd = uri[uri.rfind('/')+1:]
                
        contentType = getContentType(uriEnd)
        
        if(not checkMethod(method)):
            code = "405 Method Not Allowed"
        elif(not checkURIExists(uri)):
            code = "404 Not Found"
        else:
            code = "200 OK"
            payload = open(uri).read()
        
        response = create_response(code, payload, contentType)
        #print("\nMaking a response:\n\n{}".format(response))
        self.request.sendall(bytearray(response.encode()))
        

def checkMethod(method):
    return method == 'GET'

def checkURIExists(uri):
    return os.path.isfile(uri)

def getContentType(file):
    ext = file[file.find('.')+1:]
    if(ext == 'css'):
        return 'text/css'
    elif(ext == 'html'):
        return 'text/html'
    else:
        return ''

def create_response(code, payload, contentType):
    #now = datetime.now()
    #stamp = mktime(now.timetuple())
    #httpDate = format_date_time(stamp)
    #httpServer = "Python/6.6.6 (custom)"
    #response = "HTTP/1.1 {}\r\nDate: {}\r\nServer: {}\r\nContent_Type: {}\r\n\r\n{}".format(code, httpDate, httpServer, contentType, payload)
    simpleResponse = "HTTP/1.1 {}\r\nContent-type: {}\r\n\r\n{}".format(code, contentType, payload)
    return simpleResponse


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    
    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

