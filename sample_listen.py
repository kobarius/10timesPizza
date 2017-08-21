#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import cStringIO

# Raspberry PiのIPアドレス
host = 'localhost'
# juliusの待ち受けポート
port = 10500

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

xml_buff = ""
in_recoguout = False

def word(recv_data):
    for line in recv_data.split('\n'):
        index = line.find('WORD="')
        if index!=-1:
            line = line[index+6:line.find('"',index+6)]
            if(line!='<s>' and line!='</s>'):
                yield line


while True:
    data = cStringIO.StringIO(sock.recv(4096))
    line = data.readline()
    # 認識結果はRECOGOUTタグで返ってくるのでそこだけ抽出
    while line:
        if line.startswith("<RECOGOUT>"):
            in_recoguout = True
            xml_buff += line
        elif line.startswith("</RECOGOUT>"):
            xml_buff += line
#            print xml_buff
            print (''.join(word(xml_buff)))
            in_recoguout = False
            xml_buff = ""
        else:
            if in_recoguout:
                xml_buff += line
        line = data.readline()
sock.close()
