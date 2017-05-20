#!/usr/bin/env python

import rospy as rp
from sensor_msgs.msg import Image
from turmc.vision.cameras import *
from turmc.vision.utils import Mat2ImgMsg

#Initializes objects used in this publisher
def init():
    #Reference the global namespace
    global ted, bill, useless
    global tedPub, billPub, uselessPub
    global rate

    #Initialize the cameras
    ted = Ted()
    bill = Bill()
    useless = Useless()

    #Initialize the publishers
    tedPub = rp.Publisher('images/Ted', Image, queue_size = 5)
    billPub = rp.Publisher('images/Bill', Image, queue_size = 5)
    uselessPub = rp.Publisher('images/Useless', Image, queue_size = 5)

    #Initialize the node
    rp.init_node('ImagePublisher', anonymous = True)

    #Create a rate object set at 2 Hz
    rate = rp.Rate(2)

#Safely cleans up the camera objects
def shutdown():
    ted.release()
    bill.release()
    useless.release()

#Continously publishes images
def main():
    #Setup
    init()

    #Publishing loop
    while not rp.is_shutdown():
        tedPub.publish(Mat2ImgMsg(ted.getImage()))
        billPub.publish(Mat2ImgMsg(bill.getImage()))
        uselessPub.publish(Mat2ImgMsg(useless.getImage()))
        rate.sleep()

    #Cleanup
    shutdown()

#Boilerplate for running as a script
if __name__ == '__main__':
    try:
        main()
    except rp.ROSInterruptException:
        rp.loginfo('ImagePublisher interrupted; shutting down...')
        shutdown()
        pass
