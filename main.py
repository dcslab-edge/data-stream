#usr/bin/python3.7
#coding: UTF-8

import argparse
import json
import os
import random
import string
import time
from pathlib import Path

from sender import Sender
from data_generator import dataGenerator
from signal_manager import signalManager

class saveable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            with open(prospective_dir, 'w'): pass
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))



def main() :
    parser = argparse.ArgumentParser(description='Create Random datastrean written in data.config.json file format')
    parser.add_argument('config_dir', metavar='PARENT_DIR_OF_CONFIG_FILE', type=str, nargs='+',
                    help='Directory path where the config file (data.config.json) exist. (support wildcard *)')
    parser.add_argument('-t','--target',type=str,help='target server address to send generated data')
    parser.add_argument('-p','--port',type=int,help='target server address to send generated data')
    parser.add_argument('-i','--interval',type=int,help='interval to send data')

    parser.add_argument('-s','--save',action=saveable_dir,help='save data in specified path')
    args = parser.parse_args()
    #save_path =args.save

    data_cfg:Path = Path(args.config_dir[0]) / "data.config.json"
    data_sav:Path = Path(args.config_dir[0]) / "data.json"
    sig:signalManager = signalManager("147.46.242.201",8192)

    
    if args.interval==None : 
        interval = 1000
    else :
        interval = args.interval

    with open(data_cfg) as f:
        cfg = json.load(f)
    with open(data_sav,'w') as sv:
        generator = dataGenerator(cfg)
        sender:Sender =Sender(generator,interval,data_sav,args.target,args.port)
        conn,addr = sig.wait_for_connection()
        try:
          sig.wait_for_start_signal(conn,sender)
        except Exception as e:
          print(e)
        finally :
          conn.close()
          sig._socket.close()



if __name__=='__main__' :
    main()
