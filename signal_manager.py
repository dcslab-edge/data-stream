#python3.7
#encoding : UTF-8
import socket
import time
from data_generator import dataGenerator

class signalManager:
    def __init__(self,local_ip:str, port:int):
        self._port=port
        self._ip=local_ip
        self._socket = socket.socket()


    def wait_for_connection(self):
        self._socket.bind((self._ip,self._port))
        self._socket.listen(5)
        print("signalManger:listening at port "+str(self._port))


        while True:
            conn,addr = self._socket.accept()
            print("signalManager:connection accepted")
            return (conn,addr)

    def wait_for_start_signal(self,conn,sender,data_len=100):
        while True:
            signal=conn.recv(65536).decode()
            if signal=="start" :
                conn.send("started".encode())
                sender.sendAndSaveData(data_len)
                self.send_end_signal(conn)
                return;
            else :
                continue

    def send_end_signal(self,conn) :
        conn.send("end".encode())
        print("send end to signaler")
        conn.close()
        print("connn closed")
        self._socket.close()
        print("socket closed")



