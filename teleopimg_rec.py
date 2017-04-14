from JoystickListener import JoystickListener
import cv2
from socket import *
from time import sleep
import numpy as np

#Nuc Image Request Server. Recieves input from MotorControlBase program, and sends to the ServerApp Program
targetIP = '192.168.1.103'

port_send = 16000
serverAddress = (targetIP, port_send)

sendingSocket = socket(AF_INET, SOCK_DGRAM)

def my_func(data):
    if data['button11'] == 1.0:
        print("Button 11 was pushed")
        cam1 = cv2.VideoCapture(0) #Eventually use sam's vision library to grab the instance and grab a frame
        ret1, cam1_img = cam1.read()
        print len(cam1_img)
        #Image Compression Begins here
        img *= 1./255;
        cam1_img = cvtColor(cam1_img, cv2.COLOR_BGR2LUV);
        cam1_img = cv2.resize(cam1_img,None,fx=0.2,fy=0.2,interpolation = cv2.INTER_LANCZOS4)
        cam1_img = cv2.cvtColor(cam1_img, cv2.COLOR_BGR2GRAY)
        print len(cam1_img)
        print cam1_img.shape
        frame = cam1_img.flatten()
        print frame.shape
        data = frame.tostring()
    #img_str = cv2.imencode('.jpg', cam1_img)[1].tostring()
    #print len(img_str)
    #maybe try grab and send that tuple over, base would then run retieve() on it?
    #cam1_img = cam1_img.reshape(0,1)
        sendingSocket.sendto(data, serverAddress)


def main():
    listener = JoystickListener(15000, my_func)
    listener.startListening()

if __name__== '__main__':
    main()