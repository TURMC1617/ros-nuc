from JoystickListener import JoystickListener
import cv2
from socket import *
from time import sleep

targetIP = '192.168.1.103'

port_send = 16000
serverAddress = (targetIP, port_send)

sendingSocket = socket(AF_INET, SOCK_DGRAM)

def my_func(data):
    if data['button11'] == 1.0:
        cam1 = cv2.VideoCapture(0)
        ret1, cam1_img = cam1.read()
        #maybe try grab and send that tuple over, base would then run retieve() on it?
        #cam1_img = cam1_img.reshape(0,1)
        sendingSocket.sendto(cam1_img, serverAddress)


def main():
    listener = JoystickListener(15000, my_func)
    listener.startListening()

if __name__== '__main__':
    main()