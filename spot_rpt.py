#!/usr/bin/env python

import datetime, sys, getopt
from ClientSocket import *
from pyhamtools import dxcluster as parser
from FlexRadio import *
import argparse, time
import yaml

def now():
    ts = datetime.datetime.now(datetime.timezone.utc)
    return ts.timestamp()


def connect_cluster(host, port, call):
    retries = 0
    tn = None
    login = f'{call}\r\n'

    while retries <= 3:
        try:
            print(f'trying {host}:{port} ...')
            tn = ClientSocket()
            tn.settimeout(15)
            tn.connect(host, port)
            tn.write(login.encode())
            cluster_info = tn.read_until(b' >\r\n')
            #print(cluster_info)
            tn.write(b'sh/myfdx 30\r\n')
            
            # keep the 15 sec timeout so we 
            # can ctrl-c this thing in a reasonable
            # amount of time..
            #tn.settimeout(None)
            print('connected')
            break
        except socket.timeout:
            tn.close()
            tn = None
            print('timed out. will try again in 1 minute')
            retries += 1
            time.sleep(60)
        except Exception as e:
            print(e)
            raise
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
        except socket.timeout:
            continue
        except EOFError:
            break

def parse_args(argv):
    reparse = False
    parser = argparse.ArgumentParser()

    parser.add_argument('--call', type=str)
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=int)
    parser.add_argument('--config', type=str)
    args = parser.parse_args(argv)

    if args.config == None:
        args.config = '/usr/local/etc/flex_spots.conf'

    return args

def configure(args):
    with open(args.config,'r') as fh:
        config = yaml.safe_load(fh)
    
    # override the config file with any command line args.
    if args.host != None:
        config['cluster'][0]['host'] = args.host
    
    if args.call != None:
        config['cluster'][0]['call'] = args.call
        
    if args.port != None:
        config['cluster'][0]['port'] = args.port
    
    return config
    
def proc_perma_spots(spots, flex):
    for spot in spots:
        flex.SendPermaSpot(spot)

def main(argv):
    args = parse_args(argv)
    config = configure(args)
    
    flex = FlexRadio()
    flex.Connect()
    tn = connect_cluster(config['cluster'][0]['host'], 
                        config['cluster'][0]['port'], 
                        config['cluster'][0]['call'])
    
    if 'perma_spots' in config:
        proc_perma_spots(config['perma_spots'], flex)
    
    if tn is not None:
        proc_spots(tn, flex)
    else:
        print(f'failed to connect to {host}:{port}')

if __name__ == "__main__":
    main(sys.argv[1:])
