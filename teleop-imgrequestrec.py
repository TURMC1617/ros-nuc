#!/usr/bin/env python


import cv2
from socket import *
from time import sleep

#target Main base computer information
targetIP = '192.168.1.103'

port_recv = 15000
port_send = 16000
serverAddress = (targetIP, port_send)

#recieving port on Nuc
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', port_recv))

sendingSocket = socket(AF_INET,SOCK_DGRAM)
sendingSocket.bind(('',port_send))





def sendimg():
    print("sending image")
    #Init instance of cameras for teleop visual feedback
    cam1 = cv2.VideoCapture(0)
    cam2 = cv2.VideoCapture(1)
    ret1, cam1_img = cam1.read()
    ret2, cam2_img = cam2.read()
    cam1_img = cam1_img.reshape(0,1) #make continuous
    cam2_img = cam2_img.reshape(0,1)

    #send image size for diagnostic purposes
    cam1_imgsize = cam1_img.total() * cam1_img.elemSize();
    cam2_imgsize = cam2_img.total() * cam2_img.elemSize();

    bytes1 = send(sendingSocket, cam1_img.data, cam1_imgsize, 0)
    #delay before sending second picture, depends on latency of connection
    sleep(100)
    #bytes2 = send(sendingSocket, cam2_img.data, cam2_imgsize,0)
    
    #Try this method if above doesn't work
    #serverSocket.sendto(cam1_img.data, serverAddress)
    
    #sleep for a bit and saftely release camera objects
    sleep(50)
    cam1.release()
    cam2.release()


while True:
    message, address = serverSocket.recvfrom(1024)

    if message == "img":
	print("recv")
        sendimg()







