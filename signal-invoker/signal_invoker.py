import sys
import socket
import time
from time import sleep
from pathlib import Path
import psutil


if __name__=="__main__" :
  if(len(sys.argv)!=2):
    print("need ip address for data-stream, assuming as local host(242.201)")
    stream_addr="147.46.242.201"
  else:
    stream_addr = sys.argv[1]
    
  socket = socket.socket()
  socket.connect((stream_addr,8192))
  print("connect established")
  while 1:
    socket.send("start".encode())
    print("start signal send")
    sig = socket.recv(65536).decode()
    if sig=="started" :
      print("it is started, sparkGPU receiving all data")
    break;
  while 1:
    sig = socket.recv(65536).decode()
    if sig=="end":
      print("sending termiated, end SparkSubmit process")
      ls=[]
      for p in psutil.process_iter(attrs=["name","exe","cmdline"]):
        for x in p.info['cmdline']:
          if "SparkSubmit" in x:
            sleep(1)
            p.terminate()
      break;
      

	
