#!/usr/bin/env python

import datetime
from ClientSocket import *
from pyhamtools import dxcluster as parser
from FlexRadio import *

def now():
   ts = datetime.datetime.now(datetime.timezone.utc)
   return ts.timestamp()


def connect_cluster(host, port):
    tn = ClientSocket()
    tn.connect(host, port)
    tn.write(b'wk2x\r\n')
    cluster_info = tn.read_until(b'dxspider >\r\n')
    #print(cluster_info)
    tn.write(b'sh/myfdx 30\r\n')
    return tn

def proc_spots(tn, flex):
    while True:
        try:
            line = tn.read_until(b'\r\n').replace(b'\x07', b'').replace(b'\xa0', b' ')
            #print(line)
            try:
                spot = parser.decode_char_spot(line.decode())
                if spot:
                    spot["time"] = now()
                    
                    # convert freq to MHz
                    spot['frequency'] = spot['frequency'] / 1000.0
                    
                    flex.SendSpot(spot)
            except ValueError:
                continue
        except EOFError:
            break


def main():
    host = 'dxusa.net'
    port = 7300
    flex = FlexRadio()
    flex.Connect()
    tn = connect_cluster(host, port)
    proc_spots(tn, flex)
   
if __name__ == "__main__":
    main()

