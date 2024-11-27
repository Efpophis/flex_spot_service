#!/usr/bin/env python

import socket

class ClientSocket:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self, host, port):
        return self.sock.connect((host,port))
    
    def read(self, count=4096):
        return self.sock.recv(count)
    
    def read_until(self, delimiter):
        """Read data from a socket until a delimiter is found."""
        buffer = b""
        while True:
            data = self.sock.recv(1)
            if not data:
                raise EOFError("Socket closed before delimiter was found.")
            buffer += data
            if buffer.endswith(delimiter):
                return buffer[:-len(delimiter)]
            
    def write(self, buffer):
        return self.sock.send(buffer)
    
    def empty(self):
        self.sock.settimeout(1)
        ebuf = b''
        while True:
            try:
                ebuf += self.read()
            except socket.timeout:
                break
            except Exception as err:
                raise err
        return ebuf
