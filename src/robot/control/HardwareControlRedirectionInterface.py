#!/usr/bin/env python

import rospy as rp
from std_msgs.msg import String
from turmc.global_constants import *

#Debugging
def redirectMining(data):
    rp.loginfo('Redirecting from Mining')
    redirect(data)

#Debugging
def redirectDumping(data):
    rp.loginfo('Redirecting from Dumping')
    redirect(data)

#Debugging
def redirectNavigating(data):
    rp.loginfo('Redirecting from Navigating')
    redirect(data)

#Redirects command to MotorControlNode
def redirect(data):
    pub.publish(data)

#Initialize the node
def init():
    global pub, miningSub, dumpingSub, navigatingSub

    pub = rp.Publisher(TOPIC_MOTOR_CONTROL, String, queue_size = 5)

    rp.init_node('HardwareControlRedirectInterface', anonymous = True)

    miningSub = rp.Subscriber(TOPIC_MINING_REDIRECT, String, redirectMining)
    dumpingSub = rp.Subscriber(TOPIC_DUMPING_REDIRECT, String, redirectDumping)
    navigatingSub = rp.Subscriber(TOPIC_NAVIGATING_REDIRECT, String, redirectNavigating)

#Main loop; keeps node alive
def main():

    init()

    rp.spin()

#Boilerplate
if __name__ == '__main__':
    try:
        main()
    except rp.ROSInterruptException:
        rp.loginfo('HCRI Node interrupted; shutting down')
        pass
