

import signal
import sys
import socket
import time
from data_generator import dataGenerator,dataType
from pathlib import Path


class Sender:
    def __init__(self,gen:dataGenerator,interval,save:Path,target_ip:str,target_port:int=8000):
        self._ip:str=target_ip
        self._port:int=target_port
        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._generator = gen
        self._save = save
        self._interval = interval


    def genData(self):
        return self._generator.generateData()

    def signal_handler(self,sig, frame):
        self._socket.close()
        sys.exit(0)



    def sendAndSaveData(self,line_limit:int):
        self._socket.bind((self._ip,self._port))
        self._socket.listen(1)
        signal.signal(signal.SIGINT, self.signal_handler)
        with open(self._save,"w") as f:
            try:
                for _ in range(0,line_limit):
                    print("1 ok")
                    data =self.genData()
                    print("2 ok")
                    f.write(data+"\n")
                    print("3 ok")
                    print(data)
                    conn, addr = self._socket.accept()
                    print("4 ok")
                    conn.send(data.encode())
                    print("5 ok")
                    time.sleep(self._interval/1000)
                    conn.close()
            except Exception as e:
                print("error occurred")
                print(e)
            finally:
                self._socket.close()
                f.close()
        print("send terminated")

        # def sendData(self,data):
        #     try:
        #         print(self._ip,self._port)
        #         self._socket.connect((self._ip,self._port))
        #         print ("TCP Sender connected to "+self._ip+":"+str(self._port))
        #         print(data)
        #         self._socket.send(data.encode())
        #     except Exception as e:
        #             print("something's wrong with %s:%d. Exception is \n%s" % (self._ip, self._port, e))
        #     finally:
        #         self._socket.close()


        #
        # #TCP Client Code:
        # # TCP client example
        #
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # client_socket.connect(("www.hsd.or.kr", 5000))
        # while 1:
        #     data = client_socket.recv(512).decode()
        #     if ( data == 'q' or data == 'Q'):
        #         client_socket.close()
        #         break;
        #     else:
        #         print ("RECEIVED:" , data)
        #         data = input ( "SEND( TYPE q or Q to Quit):" )
        #         if ( data == 'q' or data == 'Q'):
        #             client_socket.send(data.encode())
        #             client_socket.close()
        #             break;
        #         else:
        #             client_socket.send(data.encode())
        # print ("socket colsed... END.")
        #
        #
