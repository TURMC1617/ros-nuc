#!/usr/bin/env python

import rospy as rp
from sensor_msgs.msg import Image
from turmc.global_constants import IMAGE_PUBLISH_FREQUENCY, TOPIC_USELESS_IMAGES
from turmc.vision.cameras import Useless
from turmc.vision.utils import Mat2ImgMsg

#Initializes objects used in this publisher
def init():
    #Reference the global namespace
    global useless, uselessPub, rate

    #Initialize the camera
    useless = Useless()

    #Initialize the publisher
    uselessPub = rp.Publisher(TOPIC_USELESS_IMAGES, Image, queue_size = 5)

    #Initialize the node
    rp.init_node('Useless', anonymous = True)

    #Create a rate object set at 1 Hz
    rate = rp.Rate(IMAGE_PUBLISH_FREQUENCY)

#Safely cleans up the camera object
def shutdown():
    useless.release()

#Continously publishes images
def main():
    #Setup
    init()

    #Publishing loop
    while not rp.is_shutdown():
        uselessPub.publish(Mat2ImgMsg(useless._getRawImage()))
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
