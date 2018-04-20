#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import cStringIO
# GPIOを制御するライブラリ
import wiringpi
# タイマーのライブラリ
import time
# 引数取得
import sys

###### motor setting #######
# GPIO端子の設定
motor1_pin = 23
motor2_pin = 24

# GPIO出力モードを1に設定する
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode( motor1_pin, 1 )
wiringpi.pinMode( motor2_pin, 1 )

###### END motor setting #######

###### julius setting #######
# Raspberry PiのIPアドレス
host = 'localhost'
# juliusの待ち受けポート
port = 10500

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

xml_buff = ""
in_recoguout = False

n_pizza=5

###### END julius setting #######

def word(recv_data):
    for line in recv_data.split('\n'):
        index = line.find('WORD="')
        if index!=-1:
            line = line[index+6:line.find('"',index+6)]
            if(line!='<s>' and line!='</s>'):
                yield line

def rotMotor(speed):
    wiringpi.digitalWrite( motor1_pin, 1 )
    wiringpi.digitalWrite( motor2_pin, 0 )

def breake():
    wiringpi.digitalWrite( motor1_pin, 1 )
    wiringpi.digitalWrite( motor2_pin, 1 )

def pizzaCB(n_called):
    print("pizza"+str(n_called))
    speed = n_called*1
    if n_called < 10:
        breake()
    else:
        rotMotor(speed)


if __name__=="__main__":
    breake()
    while True:
        try:
            data = cStringIO.StringIO(sock.recv(4096))
            line = data.readline()
            # 認識結果はRECOGOUTタグで返ってくるのでそこだけ抽出
            while line:
                if line.startswith("<RECOGOUT>"):
                    in_recoguout = True
                    xml_buff += line
                elif line.startswith("</RECOGOUT>"):
                    xml_buff += line
                    
                    words = ''.join(word(xml_buff))
                    print (words)
                    if words == "ピザ" or words == u"ピザ":
                        n_pizza+=1
                        pizzaCB(n_pizza)
                    in_recoguout = False
                    xml_buff = ""
                else:
                    if in_recoguout:
                        xml_buff += line
                line = data.readline()
        except KeyboardInterrupt:
        # CTRL+Cで終了
            sock.close()
            breake()
            print("end 10timesPizza")


