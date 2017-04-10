#!/usr/bin/env python

import pygame as pyg
import cv2
from socket import *

#target Main base computer information
targetIP = '192.168.1.100'

port = 15000
serverAddress = (targetIP, port)

#recieving port on Nuc
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', port))





def sendimg():
    print("sending image")
    #Init instance of cameras for teleop visual feedback
    cam1 = cv2.VideoCapture(0)
    cam2 = cv2.VideoCapture(1)
    ret1, cam1_img = cam1.read()
    ret2, cam2_img = cam2.read()


while True:
    message, address = serverSocket.recvfrom(1024)

    if message = "img":
        sendimg()



        at frame;
frame = (frame.reshape(0,1)); // to make it continuous

int  imgSize = frame.total()*frame.elemSize();

// Send data here
bytes = send(clientSock, frame.data, imgSize, 0))