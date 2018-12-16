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
    args = parser.parse_args()
    #save_path =args.save

    data_cfg:Path = Path(args.config_dir[0]) / "data.config.json"
    data_sav:Path = Path(args.config_dir[0]) / "data.json"


    with open(data_cfg) as f:
        cfg = json.load(f)
        if args.interval==None : 
          interval = cfg["data_submit_interval"]
        else :
          interval = args.interval
        print(cfg["host_ip"])
        print(interval)
        print(int(cfg["host_port"]))
        sig:signalManager = signalManager(cfg["host_ip"],int(cfg["host_port"]))
        generator = dataGenerator(cfg)
        sender:Sender =Sender(generator,interval,data_sav,cfg["sparkGPU_target_ip"],int(cfg["sparkGPU_target_port"]))
        conn,addr = sig.wait_for_connection()
        try:
          sig.wait_for_start_signal(conn,sender,int(cfg["total_data_submit_count"]))
          
        except Exception as e:
          print(e)
        finally :
          print("finnally")
          conn.close()
          sig._socket.close()
          f.close()




if __name__=='__main__' :
    main()
