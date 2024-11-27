#!/usr/bin/env python

import datetime
import telnetlib
import socket
from pyhamtools import dxcluster as parser

class FlexRadio:
    def __init__(self):
        self.host = ""
        self.port = 0

    def Discover(self):
        disc = {}
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 4992))
        data, addr = s.recvfrom(4096)
        if len(data) > 7:
            string = data[28:].decode()
            #print(string)
            ps = string.split(' ')
            for s in ps:
                item = s.split('=')
                disc[item[0]] = item[1]
            #print(disc)
            self.host = disc['ip']
            self.port = int(disc['port'])
            
            print(f'host: {self.host}, port: {self.port}')
                                
        s.close()
        
    def Connect(self):
        if self.port == 0:
            self.Discover(self)
        
    

def now():
   ts = datetime.datetime.now(datetime.timezone.utc)
   return ts.timestamp()

# don't need this
#def parse_shdx(raw_string):
#   data = {}
   
#   data[const.FREQUENCY] = float(raw_string[0:7])
#   data[const.DX] = re.sub(r'[^A-Za-z0-9\/]+', '', raw_string[8:19])
#   data[const.TIME] = datetime.datetime.fromsioformat(raw_string[20:37])
#   data[const.COMMENT] = re.sub(r'[^\sA-Za-z0-9\.,;\#\+\-\!\?\$\(\)\@\/]+', raw_string[38:67])
#   
#   return data


def connect_cluster(host, port):
   tn = telnetlib.Telnet(host, port)
   tn.write(b'wk2x\r\n')
   cluster_info = tn.read_until(b'dxspider >\r\n')
   print(cluster_info)
   tn.write(b'sh/myfdx 30\r\n')
   return tn

def proc_spots(tn):
   while True:
      try:
         line = tn.read_until(b'\n').decode('utf-8')
         try:
            spot = parser.decode_char_spot(line)
            if spot:
               spot["time"] = now()
               print(spot)
         except ValueError:
            continue
      except EOFError:
         break

      

def main():
    host = 'dxusa.net'
    port = 7300
    flex = FlexRadio()
    flex.Discover()
    
    tn = connect_cluster(host, port)
    proc_spots(tn)
   
if __name__ == "__main__":
    main()

