#!/usr/bin/env python

import datetime, sys, getopt
from ClientSocket import *
from pyhamtools import dxcluster as parser
from FlexRadio import *
import argparse

def now():
   ts = datetime.datetime.now(datetime.timezone.utc)
   return ts.timestamp()


def connect_cluster(host, port, call):
    tn = ClientSocket()
    tn.connect(host, port)
    login = f'{call}\r\n'
    tn.write(login.encode())
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

def parse_args(argv):
    host = ''
    port = 0
    call = ''
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--call', type=str, required=True)
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('--port', type=int, required=True)
    
    args = parser.parse_args(argv)
    
    return args.host, args.port, args.call
    

def main(argv):
    host, port, call = parse_args(argv)
    flex = FlexRadio()
    flex.Connect()
    tn = connect_cluster(host, port, call)
    proc_spots(tn, flex)
   
if __name__ == "__main__":
    main(sys.argv[1:])

