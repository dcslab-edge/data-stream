#data-stream

##Usage
    python3.7 <configuration_dir> [-t <target_server>] [-p <target_port>] [-i <interval>] [-s <data_save_path>]

사용하기 위해서는 socket 연결이 될 시작/종료 신호 노드와 데이터 처리 노드가 필요하다

데이터 처리 노드 : -t, -p 인자로 설정가능. receiver/ 경로 내의 코드를 실행할 Spark/SparkGPU 필요

시작종료 신호 노드 : data 생성 시작 신호를 보내고, 완료 신호를 받을 노드. 프로젝트의 edge-manager기능.
현재는 자동으로 포트 8192를 사용


##인자설명

configuration_dir : 설정 파일이 있는 경로, data.config.json으로 두어야 하며, 예시 파일은 data.config.template.json에서 확인가능

-t <target_server> : data가 전송될 서버 주소

-p <target_port> :  연결할 서버 포트

-i <interval> : 데이터 생성&전송 주기(ms), 기본 주기는 1000ms

-s <data_save_path> : 생성한 데이터를 저장할 장소. string형태로만 현재는 보관

##Examples 

    
시작종료 신호 노드 코드(signal_invoker.py):

    import socket                                                                                                                                                                     [0/292]
    import time
    from pathlib import Path
    
    if __name__=="__main__" :
      socket = socket.socket()
      socket.connect(("147.46.242.201",8192))
      print("connect established")
      while 1:
          socket.send("start".encode())
          print("start signal send")
          sig = socket.recv(65536).decode()
          print(sig)
          if sig=="started" :
            print("success")
            break;
            

## 실행 순서(topdown)
- main.py 실행(데이터 생성+전달 대기)
(설정경로 : ./local_config/, spark-streaming 위치 : localhost:8888)
````
python3.7 main.py ./local_config/ -t localhost -p 8888
````
- signal_invoker.py 실행
(signal_invoker 위치 : 147.46.242.206)
````
python3.7 signal_invoker.py
````
- SparkGPU streaming processor 실행
````
<<path_to_sparkGPU_bin>/spark-submit ./receiver/sparkgpu_receiver_code.py
````

###data.config.json 설명

    interval(sec) : generate & send data with defined interval. if not specified, interval value is 1 second
    configuration_dir : directory where 'data.config.json' exists (See data.config.template.json'
    maximum_data_count : total number of data
    specific_data_types : multiple objects specifying data
        {
          type : type of data(int,long,string)
          count : number of values with type
          length : size of data(int,long : max value/string : length of string)
        }
    major_data_type : type of remaining data values (non-specific)
    major_data_length : size of remaining data values


